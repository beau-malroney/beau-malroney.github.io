---
layout: page
title: "OpenMediaVault NAS Walkthrough: Old PC, Media, Backups, and Retro Gaming"
permalink: /openmediavault-old-pc-nas-walkthrough/
description: "A storage-first walkthrough for turning an old Windows PC with 16 GB RAM into an OpenMediaVault NAS with SMB shares, Jellyfin, Pi-hole, backups, Syncthing, and optional WebDAV."
---

This walkthrough turns an old Windows PC with 16 GB RAM into a storage-first home NAS running OpenMediaVault (OMV), SMB file shares, Jellyfin, Pi-hole, versioned backups, RetroArch save synchronization, and optional WebDAV.

The recommended order is intentional: get storage, permissions, backups, and restore testing right before adding media streaming, network DNS, or synchronization services.

> **Important:** A NAS is not a backup by itself. RAID, a mirror, SnapRAID, or a filesystem snapshot can help with disk or deletion failures, but critical data still needs an independent external and/or off-site backup copy.

## Target Architecture

```text
Old Windows PC
└── OpenMediaVault
    ├── OS SSD: OpenMediaVault only
    ├── SSD/NVMe: Docker app data, databases, Compose projects
    ├── HDD data pool:
    │   ├── Media/
    │   │   ├── Movies/
    │   │   ├── TV/
    │   │   ├── Music/
    │   │   └── Home-Videos/
    │   ├── Games/
    │   │   └── Installers/
    │   ├── Retro/
    │   │   ├── ROMs/
    │   │   ├── BIOS/
    │   │   ├── Saves/
    │   │   ├── Save-States/
    │   │   ├── Screenshots/
    │   │   └── Artwork/
    │   ├── Backups/
    │   │   ├── PCs/
    │   │   ├── Macs/
    │   │   ├── Server/
    │   │   └── Kopia/
    │   └── App-Backups/
    └── Docker Compose services
        ├── Jellyfin
        ├── Pi-hole
        ├── Syncthing, optional
        └── WebDAV, optional
```

## 1. Prepare the Hardware

### Recommended disk layout

| Hardware | Recommended role |
|---|---|
| 120–256 GB SATA SSD | OpenMediaVault operating system only |
| 250 GB+ SSD/NVMe, if available | Docker app data, databases, Compose projects, Jellyfin metadata/cache |
| Two or more HDDs | NAS data: media, games, retro archive, backups |
| USB external HDD | Rotated/offline backup destination |
| Wired gigabit Ethernet | Strongly recommended; use 2.5GbE if the PC, switch, and clients support it |
| UPS with USB monitoring | Recommended for orderly shutdown during an outage |

### Pre-install checklist

- [ ] Copy anything needed from the old Windows installation; the system disk will be erased
- [ ] Update BIOS/UEFI if needed
- [ ] Set SATA mode to **AHCI**, not Intel RAID/RST, unless there is a specific reason not to
- [ ] Enable booting from USB
- [ ] Set **Restore on AC Power Loss** to **Power On** if automatic recovery after outages is desired
- [ ] Use wired Ethernet rather than Wi-Fi
- [ ] Physically label disks before installation
- [ ] Check used HDDs with SMART before placing important data on them

### Choose a storage layout

| Goal | Recommended approach |
|---|---|
| Simple and dependable | Two HDDs in RAID1/mirror, ext4, plus independent external/off-site backup |
| Mixed-size drives and media archive | Separate ext4 disks first; evaluate mergerfs + SnapRAID after learning recovery procedures |
| Maximum ZFS integrity and snapshots | Consider TrueNAS SCALE instead of OMV |
| Lowest-cost proof of concept | One data disk plus an external backup; add redundancy later |

For this OMV build, use ext4 for ordinary NAS storage unless you have a deliberate reason to use another filesystem. Do not treat RAID or parity as a substitute for backups.

## 2. Install OpenMediaVault

1. Download the current OpenMediaVault x86-64 ISO from the official project.
2. Write it to an 8 GB or larger USB flash drive with Rufus, balenaEtcher, or Ventoy.
3. If practical, temporarily disconnect all disks except the intended OS SSD. This reduces the chance of formatting a data drive by mistake.
4. Boot the old PC from the installer USB.
5. Install OpenMediaVault to the dedicated OS SSD.
6. Set a strong root password and select your time zone.
7. Restart and identify the NAS IP address through the console or your router’s DHCP lease list.
8. From another computer, open:

```text
http://NAS-IP-ADDRESS/
```

9. Immediately after first login:
   - Change the web-interface credentials
   - Configure a DHCP reservation/static lease in the router, such as `192.168.1.20`
   - Apply OMV updates
   - Set a clear hostname, such as `nas`, `homelab-nas`, or `vault`
   - Configure email notifications if SMTP is available
   - Configure SMART monitoring and scheduled filesystem checks

> Do not expose the OMV management interface directly to the internet. For remote administration, use a VPN such as Tailscale or WireGuard.

## 3. Create Users, Disks, and SMB Shares

### Create user accounts

In OMV, open **Users → Users** and create a normal administrator account, such as `beau`. Do not use `root` for SMB access, Docker file ownership, or routine administration.

Suggested access model:

| Account or group | Access |
|---|---|
| `beau` | Read/write access to personal, administration, game, and service folders |
| `family` group | Read/write access to shared media and family documents |
| `media` group | Read-only or controlled write access to media folders |
| `backups` group | Write access only to backup repository folders |
| Jellyfin container user | Read-only access to media; read/write only to Jellyfin config/cache |

Record the numeric UID and GID for the user that will own Docker files. These values are useful in Compose files when containers need to create files with the correct ownership.

### Prepare and mount data disks

1. Open **Storage → Disks** and verify every drive by its model and serial number.
2. Wipe only blank disks that are being dedicated to the NAS.
3. Create filesystems, typically ext4 for a simple OMV-based NAS.
4. Mount filesystems with clear labels such as:
   - `data01`
   - `data02`
   - `docker-ssd`
   - `backup-usb`
5. Open **Storage → Shared Folders** and create the shared folders below.

```text
Media/
Media/Movies/
Media/TV/
Media/Music/
Media/Home-Videos/
Games/
Games/Installers/
Retro/
Retro/ROMs/
Retro/BIOS/
Retro/Saves/
Retro/Save-States/
Retro/Screenshots/
Retro/Artwork/
Backups/
Backups/PCs/
Backups/Macs/
Backups/Server/
Backups/Kopia/
AppData/
Compose/
App-Backups/
```

Put `AppData` and `Compose` on the dedicated SSD/NVMe where possible. Back them up to `App-Backups` on HDD storage, then include them in external/off-site backup jobs.

### Enable SMB shares

1. Open **Services → SMB/CIFS** and enable the service.
2. Create SMB shares for `Media`, `Games`, `Retro`, and any document or backup locations meant for clients.
3. Disable guest access for private or writable shares.
4. Use per-user permissions rather than a shared household write password.

Access from Windows:

```text
\\nas\Media
\\nas\Games
\\nas\Retro
```

Access from macOS Finder: **Go → Connect to Server**:

```text
smb://nas/Media
smb://nas/Retro
```

### Suggested permissions

| Share | Suggested permission model |
|---|---|
| `Media` | Family read/write for easy uploads; Jellyfin read-only |
| `Games/Installers` | Administrator read/write; optional family read-only |
| `Retro/ROMs` | Administrator read/write; emulator clients read-only |
| `Retro/BIOS` | Administrator read/write; emulator clients read-only |
| `Retro/Saves` | Administrator and sync service read/write |
| `Backups/*` | Backup client credentials/service only |
| `AppData` | Do not expose through SMB unless a specific workflow requires it |
| `Compose` | Administrator account only |

Keep ROMs and BIOS files effectively read-only from clients. Treat saves as a separate, backed-up, versioned dataset.

## 4. Install Docker Compose

Use the current OMV-Extras and OMV Compose plugin workflow. Avoid old tutorials that install Docker packages manually or use deprecated Docker tooling.

1. Install **OMV-Extras** using its current project documentation.
2. Open **System → OMV-Extras** and enable the Docker repository.
3. Open **System → Plugins** and install **openmediavault-compose**.
4. In the Compose plugin settings:
   - Set the Compose files directory to the SSD-backed `Compose` folder
   - Set Docker application data to the SSD-backed `AppData` folder
   - Do not put databases or frequently written container data on a slow or delayed-parity disk design
5. Use separate Compose projects for separate services:

```text
Compose/
├── jellyfin/
│   └── compose.yml
├── pihole/
│   └── compose.yml
├── syncthing/
│   └── compose.yml
└── webdav/
    └── compose.yml
```

6. Back up the complete `Compose/` directory, `.env` files, and `AppData/` contents.

## 5. Deploy Jellyfin

Start with Jellyfin. It is a free, self-hosted media server for organizing and streaming personal media to TV, phone, tablet, browser, and other clients.

Create `Compose/jellyfin/compose.yml`:

```yaml
services:
  jellyfin:
    image: jellyfin/jellyfin:latest
    container_name: jellyfin
    user: "1000:1000"
    environment:
      - TZ=America/Chicago
      - JELLYFIN_PublishedServerUrl=http://nas:8096
    ports:
      - "8096:8096/tcp"
      - "7359:7359/udp"
    volumes:
      - /srv/dev-disk-by-uuid-APPDATA_UUID/AppData/jellyfin/config:/config
      - /srv/dev-disk-by-uuid-APPDATA_UUID/AppData/jellyfin/cache:/cache
      - /srv/dev-disk-by-uuid-DATA_UUID/Media:/media:ro
    restart: unless-stopped
```

Replace each example `/srv/dev-disk-by-uuid-...` path with the actual mount paths shown in OMV. Replace `1000:1000` with the numeric UID:GID of the account chosen to own the files.

Deploy the project through the OMV Compose interface, then open:

```text
http://nas:8096
```

Complete the setup wizard:

1. Create the Jellyfin administrator account.
2. Add libraries:
   - Movies: `/media/Movies`
   - TV: `/media/TV`
   - Music: `/media/Music`
   - Home videos: `/media/Home-Videos`
3. Enable scheduled library scanning.
4. Start with direct play; add hardware transcoding only after testing real clients and actual playback needs.
5. Install Jellyfin clients on the household’s supported TV/streaming devices and mobile devices.

## 6. Deploy Pi-hole Safely

Pi-hole is a network-wide DNS filtering service. Because it can become critical household infrastructure, deploy it only after core NAS storage and backup functions are stable.

Create `Compose/pihole/compose.yml`:

```yaml
services:
  pihole:
    image: pihole/pihole:latest
    container_name: pihole
    hostname: pihole
    environment:
      TZ: America/Chicago
      FTLCONF_webserver_api_password: "REPLACE_WITH_A_LONG_UNIQUE_PASSWORD"
      FTLCONF_dns_listeningMode: "all"
    ports:
      - "53:53/tcp"
      - "53:53/udp"
      - "8081:80/tcp"
    volumes:
      - /srv/dev-disk-by-uuid-APPDATA_UUID/AppData/pihole/etc-pihole:/etc/pihole
    cap_add:
      - NET_ADMIN
    restart: unless-stopped
```

Deploy the project and open:

```text
http://nas:8081/admin/
```

Then:

1. Configure upstream DNS resolvers in Pi-hole.
2. Test by manually setting DNS on a single computer to the NAS IP address.
3. Verify normal browsing, streaming, game consoles, smart TVs, and work tools.
4. Add allow-list entries for services that require them.
5. Only after successful testing, update router DHCP settings to advertise the NAS IP as primary DNS.

### Pi-hole availability choices

| Design | Trade-off |
|---|---|
| One Pi-hole | Simplest; maintenance or failure can temporarily affect household DNS |
| Pi-hole plus public/ISP secondary DNS | More resilient, but clients may bypass filtering |
| Two Pi-hole instances | Best long-term availability; run the second copy on separate hardware |
| Remote Pi-hole administration | Use a VPN; never expose the management UI publicly |

> Do not advertise a public DNS provider as a secondary DHCP DNS server if it is important that every client uses Pi-hole. Many clients will bypass Pi-hole by choosing the secondary resolver.

## 7. Configure Versioned Backups with Kopia

Use Kopia as a versioned, encrypted backup solution for PCs and server data. Use an additional external disk and/or cloud destination for protection against loss of the NAS.

### Create repository locations

```text
Backups/
└── Kopia/
    ├── Windows-PCs/
    ├── Macs/
    ├── Server/
    └── Offsite-Staging/
```

Suggested workflow:

```text
Windows PCs / Macs / Steam Deck data
        ↓
Kopia or device-specific backup client
        ↓
NAS backup repository
        ↓
External USB disk or encrypted cloud copy
```

Back up these NAS-side items:

```text
Compose/
AppData/
OpenMediaVault configuration export
Jellyfin configuration/database
Pi-hole configuration
Retro/Saves/
Important documents and photos
```

### Starter backup policy

| Data | Schedule | Example retention |
|---|---|---|
| Retro saves and essential documents | Every 1–6 hours | 30 daily versions and 12 monthly versions |
| Desktop/laptop files | Daily | 30 daily and 12 monthly versions |
| Docker Compose and AppData | Nightly | 30 daily and 12 monthly versions |
| Jellyfin/Pi-hole configuration | Nightly and before updates | 30 daily versions |
| NAS data to external/cloud | Weekly minimum | Multiple historical versions where possible |

Test at least one restore immediately after the first backup. A successful backup job is not proof of recoverability until files have been restored and opened.

For full bare-metal recovery of Windows PCs, optionally add Veeam Agent or UrBackup alongside Kopia. Use Kopia for versioned files/configuration and an image backup tool when you want whole-system restoration after an SSD or PC failure.

## 8. Sync Retro Saves with Syncthing

For cross-device RetroArch saves, use Syncthing rather than granting every device broad SMB write access to the Retro library.

```text
Steam Deck RetroArch saves
        ↕
Windows RetroArch saves
        ↕
Mac RetroArch saves
        ↕
NAS Retro/Saves
```

Mount only the folders Syncthing needs into its container:

```text
Retro/Saves/
Retro/Save-States/
Retro/Screenshots/
```

Do not give Syncthing read/write access to the complete data pool unless you specifically need that.

### Safe synchronization rules

- Use the same ROM filename across devices
- Prefer in-game saves for cross-platform portability
- Treat save states cautiously because they may depend on a particular emulator core, core version, or platform
- Do not play the same game on multiple devices at the same time while two-way synchronization is enabled
- Enable NAS-side versioning/snapshots or backup history for `Retro/Saves`
- Sync saves separately from the ROM archive

## 9. Add WebDAV Only If Needed

WebDAV is optional. SMB is normally simpler and faster for home LAN access. Add WebDAV only if a specific application supports it directly, such as a backup client or a RetroArch cloud-sync setup.

| Requirement | Better approach |
|---|---|
| LAN file access | SMB |
| Secure access while away from home | Tailscale or WireGuard, then SMB/internal services |
| Application requires WebDAV | A dedicated, authenticated WebDAV service on the LAN |
| Internet-exposed WebDAV | Reverse proxy, HTTPS, strong authentication, rate limits, and careful hardening |
| RetroArch save sync | Syncthing or WebDAV; use one primary synchronization method at a time |

For the first deployment, prefer Tailscale or WireGuard for remote access. Avoid exposing WebDAV or OMV directly to the public internet.

## 10. Back Up the NAS

Use three layers of protection:

```text
Tier 1: Live NAS data
  - Media, games, documents, Retro saves, Docker configuration

Tier 2: Local independent backup
  - External USB HDD, ideally encrypted and rotated/disconnected after jobs

Tier 3: Off-site backup
  - Encrypted cloud backup, second NAS, or a drive stored away from home
```

Prioritize off-NAS backups for:

- `Retro/Saves`
- Family photos and home videos
- Documents and code
- `Compose/`
- `AppData/`
- Pi-hole configuration
- Jellyfin configuration/database
- OMV configuration export
- Kopia repository credentials, encryption keys, and recovery documentation

A media library can often be rebuilt. Family photographs, home videos, personal documents, service configuration, and game saves may be impossible to replace.

## 11. Build Order Checklist

1. [ ] Install OMV to a dedicated SSD
2. [ ] Apply updates, reserve the NAS IP, and configure SMART/email alerts
3. [ ] Format and mount data disks
4. [ ] Create users, groups, shared folders, and permissions
5. [ ] Enable SMB and validate access from Windows and macOS
6. [ ] Create the `Media`, `Games`, `Retro`, `Backups`, `AppData`, and `Compose` folder structure
7. [ ] Install OMV-Extras, Docker, and the Compose plugin
8. [ ] Deploy Jellyfin and validate local playback
9. [ ] Configure Kopia, run the first backup, and test a restore
10. [ ] Back up OMV configuration, Compose files, and Docker app data
11. [ ] Deploy Pi-hole and test on a single client before changing router DHCP DNS
12. [ ] Add Syncthing for Retro saves and confirm version history exists
13. [ ] Add internal-only WebDAV only if a specific application needs it
14. [ ] Configure external-drive and off-site backup replication
15. [ ] Document passwords, drive serials, mount paths, encryption keys, and restore steps

## Sources

- [OpenMediaVault installation documentation](https://docs.openmediavault.org/en/8.x/installation/)
- [OMV-Extras Compose plugin documentation](https://wiki.omv-extras.org/doku.php?id=omv8:omv8_plugins:docker_compose)
- [Jellyfin container documentation](https://jellyfin.org/docs/general/installation/container/)
- [Pi-hole Docker documentation](https://docs.pi-hole.net/docker/)
- [Kopia documentation](https://kopia.io/docs/)
- [Syncthing](https://syncthing.net/)

## Final Recommendation

With 16 GB RAM, use **OpenMediaVault + Docker Compose + Jellyfin + Pi-hole + Kopia + Syncthing**. Keep OMV on its own SSD, keep Docker application data on a separate SSD/NVMe where possible, and reserve HDD storage for media, games, retro content, and backup repositories.

Use SMB for ordinary home-network access. Add WebDAV only for a specific application that needs it. Build and validate the storage and restore workflow first; the NAS succeeds when it can reliably recover your data, not merely when it can run containers.
