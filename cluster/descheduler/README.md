# Descheduler

This Helm chart installs a cronjob which will reschedule pods.

The Kubernetes scheduler will not reschedule jobs that are healthy.
In cases where jobs should be scheduled on a specific node, like the DNS server node,
but that node is down, the job will be scheduled onto another node, and will
remain on that node even after the desired node is back online.

This cronjob will actively reschedule jobs during the lifecycle.
