#!/usr/bin/env python3
"""Regression checks for deep-dive source values overwritten by the build."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class DeepDiveRegressions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with (ROOT / "i18n/tools/content_deepdive.json").open(encoding="utf-8") as source:
            cls.entries = json.load(source)

    def test_weighted_grade_example_matches_formula(self):
        text = self.entries["edu/calc-4"]["examples"][0]["body"]
        self.assertIn(f"{(85 - 70 * 0.4) / 0.6:.1f}", text)
        self.assertNotIn("91.7", text)

    def test_recording_does_not_claim_lost_detail_is_restored(self):
        entry = self.entries["audio/audio-recorder"]
        text = " ".join(entry["scenarios"] + [x["body"] for x in entry["examples"]] + [x["a"] for x in entry["faqs"]])
        self.assertNotIn("保留原始精度", text)
        self.assertNotIn("若要无损素材则导出 WAV", text)
        self.assertIn("不会恢复", text)

    def test_feed_energy_example_uses_correct_units(self):
        text = self.entries["fishery/feed-protein-fat"]["examples"][0]["body"]
        self.assertIn("11.45 kJ/g", text)

    def test_withdrawal_example_warns_about_rounding_and_limits(self):
        entry = self.entries["fishery/drug-withdrawal-fish"]
        text = " ".join(entry["scenarios"] + [x["body"] for x in entry["examples"]])
        self.assertIn("向上取整", text)
        self.assertIn("说明书", text)
        self.assertNotIn("确保渔药残留低于", text)

    def test_coin_streak_counts_both_sides(self):
        entry = self.entries["fun/coin-toss-streak"]
        text = " ".join(entry["scenarios"] + [x["body"] for x in entry["examples"]])
        self.assertIn("连续正面或连续反面", text)
        self.assertIn("最长连正 = 5", text)
        self.assertNotIn("最长连正 = 6", text)

    def test_color_guess_describes_exact_four_choice_game(self):
        entry = self.entries["fun/color-guess"]
        text = " ".join(entry["scenarios"] + [x["body"] for x in entry["examples"]] + [x["a"] for x in entry["faqs"]])
        self.assertIn("4 个", text)
        self.assertIn("完全一致", text)
        self.assertNotIn("容差内", text)

    def test_riddle_scoring_and_hint_model(self):
        entry = self.entries["fun/daily-riddle"]
        text = " ".join([x["body"] for x in entry["examples"]] + [x["a"] for x in entry["faqs"]])
        self.assertIn("每级提示扣 20 分", text)
        self.assertIn("连击加成", text)
        self.assertNotIn("连击倍数", text)

    def test_balcony_sunlight_uses_page_table(self):
        entry = self.entries["gardening/balcony-sunlight"]
        text = " ".join(x["body"] for x in entry["examples"])
        self.assertIn("夏季 8 小时", text)
        self.assertIn("冬季 4 小时", text)
        self.assertIn("高层加 0.5 小时", text)

    def test_antipyretic_title_does_not_truncate_units(self):
        import _build
        with (ROOT / "i18n/tools/healthcare.json").open(encoding="utf-8") as source:
            entry = json.load(source)["antipyretic-dose"]["zh-CN"]
        title = _build.seo_tool_title(entry["title"], entry["intro"], entry["desc"], "医疗健康")
        self.assertNotIn("60 mg", title.replace("60 mg/kg", ""))

    def test_hr_turnover_uses_average_headcount(self):
        text = " ".join(x["body"] for x in self.entries["hr/analysis-29"]["examples"])
        self.assertIn("平均在职", text)
        self.assertIn("8.57%", text)

    def test_hr_training_uses_two_levels(self):
        entry = self.entries["hr/assessor-training-hr"]
        text = " ".join(entry["scenarios"] + [x["body"] for x in entry["examples"]])
        self.assertIn("前两层", text)
        self.assertIn("82.9", text)
        self.assertNotIn("四级（反应/学习/行为/结果）打分", text)

    def test_attendance_with_leave_is_not_excellent(self):
        text = self.entries["hr/attendance-stats"]["examples"][0]["body"]
        self.assertIn("良好", text)
        self.assertNotIn("95.5%（优秀）", text)

    def test_referral_roi_and_counts_are_described_accurately(self):
        entry = self.entries["hr/calc-81"]
        text = " ".join([x["body"] for x in entry["examples"]] + [x["a"] for x in entry["faqs"]])
        self.assertIn("1354.55%", text)
        self.assertIn("不自动统计", text)
        self.assertNotIn("滚动统计", text)

    def test_whitespace_options_match_actual_controls(self):
        entry = self.entries["it/whitespace"]
        text = " ".join([x["body"] for x in entry["examples"]] + [x["a"] for x in entry["faqs"]])
        self.assertIn("压成一行", text)
        self.assertIn("合并连续空格", text)
        self.assertNotIn("保留行首缩进", text)

    def test_leather_splitter_uses_pitch_not_predicted_deviation(self):
        entry = self.entries["leather/xueyunhoudukongzhi"]
        text = " ".join(entry["scenarios"] + [x["body"] for x in entry["examples"]])
        self.assertIn("1000 × 进给速度 ÷ 转速", text)
        self.assertIn("2.00 mm/rev", text)
        self.assertNotIn("厚度偏差(mm) =", text)
        with (ROOT / "i18n/tools/leather.json").open(encoding="utf-8") as source:
            intro = json.load(source)["xueyunhoudukongzhi"]["zh-CN"]["intro"]
        self.assertNotIn("确保皮革", intro)
        self.assertIn("实测", intro)

    def test_contract_generator_uses_inputs_and_rejects_out_of_range(self):
        entry = self.entries["life/generator-price"]
        text = " ".join(x["body"] for x in entry["examples"])
        self.assertIn("单价", text)
        self.assertIn("提示", text)
        self.assertNotIn("按边界取值", text)

    def test_discount_calculator_does_not_claim_coupon_support(self):
        entry = self.entries["marketing/marketing-discount-rate"]
        text = " ".join(x["a"] for x in entry["faqs"])
        self.assertIn("不含券", text)
        self.assertNotIn("本工具按「原价×折扣系数−券」", text)

    def test_fish_pond_desilting_subtracts_retained_layer(self):
        text = self.entries["fishery/pond-desilting"]["examples"][0]["body"]
        self.assertIn("500 m³", text)
        self.assertIn("7500 元", text)
        self.assertNotIn("667 m³", text)

    def test_stocking_density_converts_grams_to_kilograms(self):
        entry = self.entries["fishery/stocking-density"]
        text = entry["examples"][0]["body"]
        self.assertIn("15/1000", text)
        self.assertIn("32000 尾/亩", text)
        self.assertIn("160000 尾", text)
        self.assertNotIn("默认参数", text)
        self.assertIn("未配增氧", entry["faqs"][0]["a"])

    def test_sprinkler_example_converts_minutes_to_hours(self):
        text = self.entries["fire-rescue/sprinkler-design"]["examples"][0]["body"]
        self.assertIn("62.4 m³", text)
        self.assertIn("124.8 m³", text)

    def test_clinical_lab_example_describes_inr(self):
        entry = self.entries["clinical-lab/convert-39"]
        text = " ".join(x["body"] for x in entry["examples"])
        self.assertIn("INR", text)
        self.assertNotIn("胆固醇", text)

    def test_detailed_sections_survive_build_data_replacement(self):
        for slug, phrase in {
            "science/fibonacci": "快速倍增",
            "signal/mod-index-am": "边带功率占比",
            "life/phone-lookup": "号码",
            "image/wechat-cover-maker": "rgba(0,0,0,0.35)",
        }.items():
            entry = self.entries[slug]
            body = " ".join(x["body"] for x in entry.get("examples", []))
            self.assertIn(phrase, body, slug)
            if slug in ("science/fibonacci", "signal/mod-index-am"):
                self.assertGreater(len(body), 900, slug)

    def test_annual_leave_uses_365_day_denominator(self):
        entry = self.entries["hr/annual-leave-prorate"]
        text = " ".join([x["body"] for x in entry["examples"]] + [x["a"] for x in entry["faqs"]])
        self.assertIn("292/365", text)
        self.assertNotIn("分母用当年实际天数", text)


if __name__ == "__main__":
    unittest.main()
