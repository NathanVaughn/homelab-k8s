# MongoDB Migration

1. Set the namespace variable to allow for copy and paste (optional):

    ```
    export OMADA_NS="omada"
    ```

2. Scale down the controller:

    ```
    flux suspend kustomization flux-system
    kubectl -n "${OMADA_NS}" scale statefulset omada-deployment --replicas=0
    ```

3. Temporarily allow privileged pods; update the namespace required (if required):

    ```
    # Store original values
    ORIGINAL_ENFORCE=$(kubectl get namespace "${OMADA_NS}" -o jsonpath='{.metadata.labels.pod-security\.kubernetes\.io/enforce}' 2>/dev/null || echo "")
    ORIGINAL_AUDIT=$(kubectl get namespace "${OMADA_NS}" -o jsonpath='{.metadata.labels.pod-security\.kubernetes\.io/audit}' 2>/dev/null || echo "")
    ORIGINAL_WARN=$(kubectl get namespace "${OMADA_NS}" -o jsonpath='{.metadata.labels.pod-security\.kubernetes\.io/warn}' 2>/dev/null || echo "")

    # Set the omada namespace to privileged (temporarily)
    kubectl label namespace "${OMADA_NS}" pod-security.kubernetes.io/enforce=privileged --overwrite
    kubectl label namespace "${OMADA_NS}" pod-security.kubernetes.io/audit=privileged --overwrite
    kubectl label namespace "${OMADA_NS}" pod-security.kubernetes.io/warn=privileged --overwrite
    ```

4. Verify the deployment is stopped:

    ```
    kubectl -n "${OMADA_NS}" get pods -l app=omada
    ```

5. Apply the migration job:

    ```
    kubectl -n "${OMADA_NS}" apply -f cluster/omada/upgrade/job.yaml
    ```

6. Monitor the migration progress:

    ```
    # Watch the job status
    kubectl -n "${OMADA_NS}" get job omada-mongodb-migration -w

    # Follow the migration logs
    kubectl -n "${OMADA_NS}" logs -f job/omada-mongodb-migration
    ```

7. Verify migration completion:

    ```
    # Check if job completed successfully
    kubectl -n "${OMADA_NS}" get job omada-mongodb-migration

    # Review final logs
    kubectl -n "${OMADA_NS}" logs job/omada-mongodb-migration
    ```

8. Remove the namespace security labels (if required):

    ```
    # Restore or remove labels based on original values
    [ -n "${ORIGINAL_ENFORCE}" ] && kubectl label namespace "${OMADA_NS}" pod-security.kubernetes.io/enforce="${ORIGINAL_ENFORCE}" --overwrite || kubectl label namespace "${OMADA_NS}" pod-security.kubernetes.io/enforce- 2>/dev/null || true
    [ -n "${ORIGINAL_AUDIT}" ] && kubectl label namespace "${OMADA_NS}" pod-security.kubernetes.io/audit="${ORIGINAL_AUDIT}" --overwrite || kubectl label namespace "${OMADA_NS}" pod-security.kubernetes.io/audit- 2>/dev/null || true
    [ -n "${ORIGINAL_WARN}" ] && kubectl label namespace "${OMADA_NS}" pod-security.kubernetes.io/warn="${ORIGINAL_WARN}" --overwrite || kubectl label namespace "${OMADA_NS}" pod-security.kubernetes.io/warn- 2>/dev/null || true
    ```


9. Update and apply your k8s deployment manifest with the new v6 image and then manually scale the deployment back up (if required):

    ```
    kubectl apply -f cluster/omada/deployment.yaml
    kubectl -n "${OMADA_NS}" scale statefulset omada-deployment --replicas=1
    ```

10. Commit the changes to main

    ```
    flux reconcile source git flux-system
    flux resume kustomization flux-system
    ```

11. Job clean up (optional):

    ```
    # job will automatically be removed after 24 hours but you can clean it up manually
    kubectl -n "${OMADA_NS}" delete job omada-mongodb-migration
    ```