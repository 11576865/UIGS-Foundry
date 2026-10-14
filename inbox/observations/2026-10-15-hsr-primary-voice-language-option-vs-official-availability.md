# Observation: HSR primary voice-language picker mixes metadata choice with official availability

Date: 2026-10-15
Project: `11576865/HSR-Voice-Archive-Builder`
State: **Observed in main source; UI change not requested or implemented**
Evidence: current product source plus official platform/HoYoverse public language documentation

## User-triggered question

The user noticed `Русский` (ru) in the primary audio language selector and asked whether Honkai: Star Rail had introduced Russian voice-over.

Product UI: `app/static/index.html` statically lists `<option value="ru">Русский</option>` in `quickAudioLanguage` and in a manual-project audio-language select. This field is a declaration about user-provided audio resources. It is not a provider catalog or an official download capability.

Product source: `app/game_profiles.py` provides HSR remote text indices only for `en`, `zh-CN`, `ja`, `ko`. `app/quick.py` uses this source-language family and can rely on same-stem LAB text for otherwise unsupported source languages. It does not establish an HSR Russian voice-over pack.

Independent public sources checked 2026-10-15:
- https://www.playstation.com/en-us/games/honkai-star-rail/ lists Voice: Chinese/English/Japanese/Korean, and Russian among Screen Languages.
- https://hsr.hoyoverse.com/en-us/news/113017?type=news_all explicitly distinguishes supported voice packs from supported text languages.
- https://store.epicgames.com/zh-hant/p/honkai-star-rail likewise lists only Chinese/English/Japanese/Korean audio and Russian text.
- July 2026 report on version 4.4 Russian localization concerns text refinements, not additional Russian voice actors: https://ixbt.games/en/news/2026/07/15/v-honkai-star-rail-44-izmenili-russkuiu-lokalizaciiu-mihoyo-rasskazala-pro-dorabotku-perevoda-igry.html

## Inference and scope

Showing an unsupported game voice language as an undifferentiated choice risks being read as an official language availability claim; no runtime code failure or proven download misrouting was observed here. Generic software may legitimately accept user-provided Russian audio with accurate metadata. Contextual labeling can separate *official game voice-over availability* from *custom/external package declared language* and from *supported text index language*.

Intake dedup: searched Foundry for Russian voice, unsupported voice language, voice language selection, capability available. Adjacent general capability records exist; no corresponding HSR picker observation found. This is a source-supported **Observation**, not a Canonical pattern, implemented fix, or confirmed actual Russian voice pack.

Related families for future review: capability catalog/availability, explicit provider-vs-user asset provenance, labels that distinguish data fields from verified supported features.

No Canonical promotion; no product code modifications from this question.
