# sample attack cases
# python3 src/attack_harness.py \
#   --case-path data/sample_attack_cases.jsonl \
#   --case-id A001 \
#   --out-path results/a001.json


# simulated attack cases
# python3 src/attack_harness.py \
#   --case-path data/simulated_attack_cases.jsonl \
#   --out-path results/simulated_attack_runs.json

# mcp live attack cases
# python3 src/attack_harness.py \
#   --case-path data/mcp_live_attack_cases.jsonl \
#   --case-id L104 \
#   --out-path results/l104.json

# # skill live attack cases
# python3 src/attack_harness.py \
#   --case-path data/skill_live_attack_cases.jsonl \
#   --case-id K201 \
#   --out-path results/k201.json


# python3 src/attack_harness.py \
#   --case-path data/skill_live_attack_cases.jsonl \
#   --case-id K202 \
#   --out-path results/k202.json

# # web search
# python3 src/attack_harness.py \
#   --case-path data/web_search_live_attack_cases.jsonl \
#   --case-id W301 \
#   --out-path results/w301.json

# # rag
# python3 src/attack_harness.py \
#   --case-path data/rag_live_attack_cases.jsonl \
#   --case-id R302 \
#   --out-path results/r302.json

# email via virtual mail
python3 src/attack_harness.py \
  --case-path data/email_workspace_attack_cases.jsonl \
  --out-path results/email_workspace_attack_runs.json

# virtual mail system
# python3 src/virtual_mail_system.py init --root virtual_mail --reset
# python3 src/virtual_mail_system.py seed --root virtual_mail --scenario procurement_footer
# python3 src/virtual_mail_system.py list --root virtual_mail --mailbox ops-assistant --folder inbox
