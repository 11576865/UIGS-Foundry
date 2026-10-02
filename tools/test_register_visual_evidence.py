#!/usr/bin/env python3
from __future__ import annotations
import json,struct,sys,tempfile,unittest,zlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import register_visual_evidence as r

def png(path:Path,w:int=3,h:int=2):
    sig=b"\x89PNG\r\n\x1a\n";ihdr=struct.pack(">IIBBBBB",w,h,8,2,0,0,0)
    def chunk(t,data):return struct.pack(">I",len(data))+t+data+struct.pack(">I",zlib.crc32(t+data)&0xffffffff)
    raw=b"".join(b"\x00"+b"\x00\x00\x00"*w for _ in range(h))
    path.write_bytes(sig+chunk(b"IHDR",ihdr)+chunk(b"IDAT",zlib.compress(raw))+chunk(b"IEND",b""))

class Tests(unittest.TestCase):
    def test_png_size(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"x.png";png(p,7,5);self.assertEqual(r.png_size(p),(7,5))
    def test_declared_landscape_rejects_portrait_png(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);contract=root/"c.json";image=root/"x.png";out=root/"m.json";png(image,5,9)
            contract.write_text(json.dumps({"platform":"android","captures":[{
                "id":"A","surface_ids":["S"],"adapter":"android-emulator-screencap",
                "evidence_level":"production-rendered","output_name":"x.png",
                "device":{"orientation":"landscape"}
            }]}),encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"declared landscape"):
                r.register(contract,"A","o/r","abcdef0",image,out)

    def test_declared_landscape_accepts_landscape_png(self):
        r.assert_declared_orientation({"device":{"orientation":"landscape"}},9,5)

    def test_contract_lookup_rejects_unknown(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);contract=root/"c.json";image=root/"x.png";out=root/"m.json";png(image)
            contract.write_text(json.dumps({"platform":"web","captures":[]}),encoding="utf-8")
            with self.assertRaises(ValueError):r.register(contract,"X","o/r","abcdef0",image,out)
if __name__=="__main__":unittest.main()
