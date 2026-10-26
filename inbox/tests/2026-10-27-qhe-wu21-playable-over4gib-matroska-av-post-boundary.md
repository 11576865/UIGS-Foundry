# WU21: playable Matroska audio/video after the 4 GiB file offset

- Date: 2026-10-27
- Project: `11576865/Quick-Automatic-Hardsub-Encoder`
- State: **IMPLEMENTED, exact-head hosted Windows evidence pending**
- Implementation PR: [#148](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/148), initial Head `586bb58e4e24db81b5c67045a888a069820e205e`
- Test class: *distinct real-media container/packet-offset and decode acceptance*, not a new Canonical requirement.

## Gap and dedup

Previously accepted [WU20](https://github.com/11576865/UIGS-Foundry/blob/main/inbox/tests/2026-10-26-qhe-wu20-over4gib-native-publish-boundary.md) proves that the production `Copy-NativeStageToOutputTemporary` / `Publish-NativeProtectedOutput` system copies and publishes a **4 GiB + 64 KiB generic binary** on actual Windows filesystems, with whole-file SHA and a partial-copy failure. It does **not** prove real >4 GiB Matroska demux/decode. WU19's real 96 MiB different-volume file and failed-write oracle is also distinct. Foundry searches for WU21, Matroska packet after 4 GiB and EBML Void validation returned no duplicate WU21 test. Record one bounded Test only, no automatic Canonical promotion.

## Proposed hosted Windows acceptance

PR #148 adds a standalone Windows `windows-wu21-over4gib-playable-mkv.yml` CI plus a Node fixture builder and a Windows PowerShell acceptance. Actual FFmpeg encodes **6 s of 256×144 H.264/8 fps (48 frames) with AAC** as a live Matroska with several genuine AV Clusters. The builder adds **five valid segment-level EBML Void elements** (four × 1 GiB plus 64 KiB), placed between actual Clusters, with source file only marked NTFS sparse. A local non-hosted prototype established FFprobe can traverse these multiple small EBML Void elements and decode H.264; by contrast one single >4 GiB Void element resulted in an unacceptable long-running scan and was rejected as a test-fixture design.

The hosted oracle must confirm ALL of:
- FFprobe reads **complete** H.264 and AAC stream frame counts, not just the header; real H.264 **and** AAC packet absolute file offsets must include **both below 64 KiB and above 4 GiB**.
- FFmpeg truly decodes the full video and audio streams into independent `framemd5` manifests **before** publishing.
- Windows `GetDiskFreeSpaceEx` confirms capacity for the **entire** >4 GiB real output stream plus 1 GiB headroom, not mock capacity or test skip.
- The product's **unchanged** `Copy-NativeStageToOutputTemporary` transfers all source bytes into a normal (non-sparse) target-volume temporary output, with complete SHA-256 equivalence and the original user-selected output unchanged until commit.
- The unchanged product `Publish-NativeProtectedOutput` publishes atomically with destination file identity safeguards. Then FFprobe rechecks video/audio packets >4 GiB and full frame counts; FFmpeg decodes both streams again; independent post-publish `framemd5` SHA-256 equals pre-publish; original/published whole-file SHA-256 equals. PowerShell process working set stays bounded.
- Insufficient real output space, any demux/decode error, packet-offset failure or source/destination mismatch must FAIL Windows CI, rather than be waived.

## Essential claim boundary

This is a **valid container with real, decodable media packets after 4 GiB offset**, but contains only **six seconds of actual encoded audio/video**, and its multi-GiB size comes from compliant Matroska EBML Void padding. It is neither a 4 GiB actual film, a real 4 GiB encoded payload, nor proof of subtitle burn-in, long-film quality, physical Windows UI player playback, USB/network output, in-copy disk depletion or uninterrupted long-term media decode. These must be independently tested before claiming full product acceptance.

At intake PR #148 actual Windows CI was **in progress**. Leave implementation/evidence state PENDING for exact-head hosted Windows outcome, not Pending because the Foundry write failed. Do not change Canonical.
