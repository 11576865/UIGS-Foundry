#!/usr/bin/env bash
set -euo pipefail

OUTDIR="$GITHUB_WORKSPACE/domains/interface-grammar/visual-evidence/images/ASS"
mkdir -p "$OUTDIR"

adb shell settings put system accelerometer_rotation 0
adb shell settings put system user_rotation 0
adb shell cmd window user-rotation lock 0 || true
adb shell wm size 1600x1000
adb shell wm density 240
adb shell settings put system font_scale 1.0
adb shell cmd uimode night yes || true

adb install -r "$GITHUB_WORKSPACE/.capture/ass/app/build/outputs/apk/debug/app-debug.apk"
adb shell am force-stop io.github.assworkbench.app
adb shell am start -W -n io.github.assworkbench.app/.MainActivity
sleep 5
adb exec-out screencap -p > "$OUTDIR/ASS.EDITOR_SHELL.EMULATOR_LANDSCAPE.png"
test -s "$OUTDIR/ASS.EDITOR_SHELL.EMULATOR_LANDSCAPE.png"
python "$GITHUB_WORKSPACE/tools/assert_png_orientation.py" "$OUTDIR/ASS.EDITOR_SHELL.EMULATOR_LANDSCAPE.png" landscape

adb install -r "$GITHUB_WORKSPACE/.capture/ass/app/build/outputs/apk/androidTest/debug/app-debug-androidTest.apk"
adb shell am instrument -w -e class io.github.assworkbench.app.UigsVisualCaptureInstrumentedTest io.github.assworkbench.app.test/androidx.test.runner.AndroidJUnitRunner

python - <<'PY' > "$RUNNER_TEMP/ass-instrumented-captures.list"
import json
data=json.load(open(".capture/ass/.uigs/ui-visual-capture.json",encoding="utf-8"))
for capture in data["captures"]:
    if capture.get("build",{}).get("test_class"):
        print(capture["id"]+"|"+capture["output_name"])
PY

while IFS='|' read -r ID FILE; do
  test -n "$ID"
  adb exec-out run-as io.github.assworkbench.app cat "files/$FILE" > "$OUTDIR/$FILE"
  test -s "$OUTDIR/$FILE"
  python "$GITHUB_WORKSPACE/tools/assert_png_orientation.py" "$OUTDIR/$FILE" landscape
done < "$RUNNER_TEMP/ass-instrumented-captures.list"
