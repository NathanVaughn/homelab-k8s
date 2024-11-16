1. Download desired Ubuntu image
2. Create bootable flash drive
3. Run `prep.py`
4. Add `autoinstall.yaml` to flash drive root
5. Modify `boot/grub.cfg` to include `autoinstall` in the `linux` command

References:

- <https://canonical-subiquity.readthedocs-hosted.com/en/latest/tutorial/providing-autoinstall.html#providing-autoinstall>
