# Where ExamGOAL's key differs from NTA's final key

Found by `tools/compare_examgoal_keys.py` (ExamGOAL's copies of our 38 NTA shifts) and **checked by eye**, both papers' images side by side. NTA's final key is still the answer used for marking; the app's answer review shows a note on these questions ("Answer keys differ ... needs more pondering"). MCQ option numbers are NTA's numbering.

Coverage: all numericals that could be paired, and the MCQs of the 2026 papers (ExamGOAL keeps NTA's option order there). Most 2023 and 2024 MCQs could NOT be compared: ExamGOAL's copies of those papers list the options in a different order and the OCR cannot pair formula options reliably.

| Question | Type | NTA final key | ExamGOAL key | Check | Claude's solution |
|---|---|---|---|---|---|
| JEE Main 2023 (Session 2), 6 Apr Shift 2, Q.60 | NUM | 99 | 101 | same question, keys differ | Claude agrees with NTA (note: NTA's 99 uses g = 9.8 m/s^{2}; g = 10 would give 101.) |
| JEE Main 2023 (Session 2), 10 Apr Shift 2, Q.27 | NUM | 5 | 4 | ExamGOAL copy has different numbers in the question (not shown in the app) | Claude agrees with NTA (note: Teacher look: the exact value is 4 + ln 3 ≈ 5.10; NTA's key gives the nearest integer, 5.) |
| JEE Main 2023 (Session 2), 10 Apr Shift 2, Q.82 | NUM | 4 | 3 | same question, keys differ | Claude agrees with NTA (note: Teacher look: NTA's 4 counts XeF_{4} by its central atom (2 lone pairs) while N_{2} and CO are counted as whole molecules; counting every lone pair, only H_{2}O, N_{2}, CO qualify (3).) |
| JEE Main 2023 (Session 2), 12 Apr Shift 1, Q.23 | NUM | 944 | 1260 | same question, keys differ | Claude agrees with NTA (note: Checked by brute force. NTA counts only non-constant APs (abc or cba); counting aaa as an AP too gives 1208.) |
| JEE Main 2023 (Session 2), 13 Apr Shift 1, Q.83 | NUM | 800 | 400 | same question, keys differ | Claude agrees with NTA |
| JEE Main 2023 (Session 2), 13 Apr Shift 1, Q.89 | NUM | 5 | 4 | same question, keys differ | Claude agrees with NTA (note: Counts alkenes from all three tertiary cations reachable by 1,2-shifts.) |
| JEE Main 2024 (Session 2), 5 Apr Shift 1, Q.27 | NUM | 72 | 198 | same question, keys differ | Claude agrees with NTA |
| JEE Main 2024 (Session 2), 6 Apr Shift 1, Q.81 | NUM | 661 | 658 | same question, keys differ | Claude agrees with NTA |
| JEE Main 2024 (Session 1), 30 Jan Shift 2, Q.3 | MCQ | 2 | 4 | same question, keys differ | Claude agrees with NTA (note: Statement II is true only vacuously: its hypothesis can never hold. This matches NTA's key.) |
| JEE Main 2024 (Session 1), 30 Jan Shift 2, Q.88 | NUM | 3 | 6 | same question, keys differ | Claude agrees with NTA (note: NTA's key (3) counts optically active products, one per structure. Counting each enantiomer separately would give 6. Worth a teacher look.) |
| JEE Main 2024 (Session 1), 31 Jan Shift 1, Q.83 | NUM | 4 | 3 | same question, keys differ | Claude agrees with NTA |
| JEE Main 2024 (Session 1), 31 Jan Shift 2, Q.86 | NUM | 4 | 8 | same question, keys differ | Claude disputes NTA's key: gets 8 |
| JEE Main 2026 (Session 2), 2 Apr Shift 2, Q.50 | NUM | 60 | 15 | same question, keys differ | Claude agrees with NTA (note: Read with the sphere rotating about its own diameter (the axis shown through its centre), which matches NTA's key.) |
| JEE Main 2026 (Session 2), 6 Apr Shift 1, Q.50 | NUM | 600 | 989 | same question, keys differ | Claude disputes NTA's key: gets 989 |
| JEE Main 2026 (Session 2), 6 Apr Shift 1, Q.67 | MCQ | 2 | 3 | same question, keys differ | Claude agrees with NTA (note: NTA's key (option 2) reads step (ii) as ring alkylation. An acid-catalysed addition to the COOH (tert-butyl benzoate, option 3) is also chemically plausible, and Friedel–Crafts on a deactivated ring is normally sluggish. Agreed with the key; a chemistry teacher may want to discuss it.) |
| JEE Main 2026 (Session 2), 8 Apr Shift 2, Q.13 | MCQ | 1 | 4 | same question, keys differ | Claude agrees with NTA |
| JEE Main 2026 (Session 2), 8 Apr Shift 2, Q.64 | MCQ | 3 | 2 | same question, keys differ | Claude agrees with NTA (note: JEE convention: NTA applies Hückel's rule to the whole molecule, so the dihydronaphthalene is not counted even though it contains a benzene ring (same convention in JEE Main 2024, 27 Jan Shift 1, Q89). In ordinary usage it would be called an aromatic compound. Worth a teacher look.) |
