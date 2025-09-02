set -e

python util/isr_llm_util/generate_household_cases.py --num_cases 200 --out_dir ./test_scenario
echo "1. Run ISR-LLM"
python baseline/isr_llm.py --logdir ./run_log/isr_llm
#echo "2. Run Self_correct"
#python baseline/self_correct.py --logdir ./run_log/self_correct
#echo "3. Run Cap"
#python baseline/cap.py --logdir ./run_log/cap
#echo "4. Run Delta"
#python baseline/delta.py