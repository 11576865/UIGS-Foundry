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

## Exact-head hosted Windows proof and main merge

[QHE PR #148](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/148), exact Head `586bb58e4e24db81b5c67045a888a069820e205e`, **2/2 applicable CI SUCCESS**, including actual [Windows WU21 run 40392389711](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/actions/runs/40392389711) and UIGS Evidence Coverage. The required independently obtained Windows job log states:

```
WU21 REAL OVER-4GIB PLAYABLE MATROSKA PASS:
 bytes=4295199928
 videoFrames=48
 audioFrames=282
 packetsAfter4GiB=true
 fullSha256=F40A3486BD12D348DEE25C3CDAD22E70A5E138BE9AD0F63F56FB5C28919EB0CF
 decodedVideoHash=06F92F738DFF836C9688EE5826420111832C36A53F914ABFA22E52D7312206FD
 decodedAudioHash=73C6836D269719BC57C88775294A1683DE38F0BC3208E972ADCED8916B26801F
 peakWorkingSetBytes=112803840
 encodedPayloadOver4GiB=false
 sparseInputEbmlVoid=true
 regularOutputCopy=true
```

The real output file exceeded unsigned 4 GiB. **Actual H.264 and AAC packet offsets** occurred before and after the 4 GiB position and both streams were fully demuxed and decoded before and after the production `Copy-NativeStageToOutputTemporary` / `Publish-NativeProtectedOutput` transaction. Output stage and final destination matched the full source SHA-256, video and audio decoded framemd5 manifest digests were independently identical, and the old user target survived until atomic commit. Windows process peak working set was about 107.6 MiB. Unlike WU20, this validates a genuinely decodable MKV container with post-4GiB AV packet offsets; unlike a full movie encode, the **encoded media payload is only six seconds** and logical size is enlarged with standard EBML Void filler.

PR #148 was squash-merged into `main@1e1c8b6f90d5de815a6c3da003fac403a43bcf29`. Independent post-merge GitHub reads located its FFmpeg/EBML fixture builder, full FFprobe/FFmpeg audio/video acceptance, exact Windows workflow and the unchanged WU19 production stream copier/publisher in the actual main branch. No UI or codec production code was changed by this test-only PR.

**Scope**: `EXACT_HEAD_WINDOWS_PLAYABLE_4GIB_CONTAINER_VERIFIED_AND_MAIN_MERGED`. NOT proof of 4GiB of actually encoded media, long feature-film playback and codec quality, real player UI/physical-device interoperability, >4GiB SMB/USB/cloud delivery, in-flight disk-full, real ASS subtitles burned into a 4GiB video or long-duration latency. These remain independent work items. No Canonical promotion and no Pending connector write.
