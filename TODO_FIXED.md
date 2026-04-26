# FitAI Error Fixes - Step-by-Step Progress

## Current Status
✅ Plan approved: Fix NameError + syntax issues only (no new features)

## Steps to Complete

### 1. Fix app.py (NameError: workout undefined) ✅
- [✅] Move debug `st.write("DEBUG workout:", workout)` after `workout = results.get("workout", {})` in `show_generate_plan()`
- [✅] Remove nested `def show_login():` duplication
- [✅] Fix `utils.get_weight_chart_data(profile).set_index('date')` - handle dict return

### 2. Fix utils.py (duplicate functions) ✅
- [✅] Remove duplicate `log_workout`, `calculate_streak`, `get_progress_stats`, `get_weight_chart_data`
- [✅] Keep single clean versions at end

### 3. Fix ml_model.py (TypeError tuple vs list) ✅
- [✅] Change `MIXED_MEAL_PLANS` tuple concatenation `()` to list `[]`

### 4. Update TODO files & Test
- [ ] Update TODO_PROGRESS.md: Mark app.py/utils.py complete
- [ ] Test: `streamlit run app.py`
- [ ] Clean cache: `rmdir /s __pycache__`
- [ ] Verify: Login → Dashboard → Generate Plan (no crash)

### 5. Completion
- [ ] attempt_completion with results

**Next:** Test the app and complete!

**Next:** Execute step-by-step, updating this TODO after each file fix.

