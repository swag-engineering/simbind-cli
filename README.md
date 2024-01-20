# Simbind CLI

Project created to test integrity of Matlab Exporter and Architect modules, since in real example they will run in
different containers.

```bash
python -m simbind \                                                                                                     2 ✘  simbind_cli  
--slx-path=/path/to/model.slx \
--pkg-name=lol_kek_223 \
--exporter-out-dir=tmp/sim \
--models-out-dir=tmp/models \
--wheel-out-dir=tmp/wheel \
--overwrite
```