# dice_Race_expectation_simulator_11.py

import streamlit as st
import random
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib

from matplotlib import font_manager

plt.rcParams["font.family"] = "IPAexGothic"
# ==================================================
# タイトル
# ==================================================


st.title("サイコロゲーム（期待値と勝率の探究） Ver.11")

st.info(
"""
【探究テーマ】

期待値が同じなら、勝率も同じになるでしょうか？

このシミュレーションでは、
異なるサイコロでレースを行い、

・期待値（平均の進み方）
・分散（出目のばらつき）
・標準偏差（ばらつきの大きさ）

と勝率との関係を調べます。

【考えてみよう】

① 期待値が同じサイコロなら公平だろうか？

② 出目のばらつきが大きいサイコロは有利だろうか？

③ ゴールまでの距離が変わると結果はどう変わるだろうか？

【実験例】

サイコロA
1,2,3,4,5,6

サイコロB
1,1,1,1,1,16

この2つのサイコロの期待値は同じです。

しかし勝率も同じになるでしょうか。

予想してから実験してみましょう。
"""
)


# ==================================================
# 勝率計算方法
# ==================================================

calc_mode = st.radio(
    "勝率の計算方法を選んでください",
    (
        "Aの単独勝ちのみ数える",
        "同時ゴールを勝ちに含める",
        "同時ゴールを引き分け扱いにする",
        "同時ゴールを除いて計算する"
    )
)

# ==================================================
# グラフ表示設定
# ==================================================

show_steps_graph = st.radio(
    "手数分布グラフの表示",
    ("表示する", "表示しない")
)


# ==================================================
# 探究モード
# ==================================================

st.header("探究モード")

show_statistics = st.checkbox(
    "期待値・分散・標準偏差を表示する",
    value=False
)

show_distribution = st.checkbox(
    "出目分布ヒストグラムを表示する",
    value=False
)


# ==================================================
# サイコロ設定
# ==================================================

st.header("サイコロの設定")

dice_A = st.text_input(
    "サイコロAの出目（カンマ区切り）",
    "1,2,3,4,5,6"
)

dice_B = st.text_input(
    "サイコロBの出目（カンマ区切り）",
    "1,1,1,1,1,16"
)

try:
    dice_A = list(map(int, dice_A.split(",")))
    dice_B = list(map(int, dice_B.split(",")))

except ValueError:
    st.error("サイコロの入力形式が正しくありません")
    st.stop()

# ==================================================
# ゴールと試行回数
# ==================================================

goal = st.number_input(
    "ゴールの数",
    value=20,
    min_value=1
)

n = st.number_input(
    "試行回数 n",
    value=100,
    min_value=1
)

# ==================================================
# 実行
# ==================================================

if st.button("スタート"):

    n = int(n)

    A_wins = 0
    B_wins = 0
    same = 0

    A_steps_list = []
    B_steps_list = []

    A_win_rate_list = []
    B_win_rate_list = []

    # ----------------------------------------------
    # シミュレーション
    # ----------------------------------------------

    for trial in range(n):

        A_pos = 0
        B_pos = 0

        A_steps = 0
        B_steps = 0

        while A_pos < goal and B_pos < goal:

            A_pos += random.choice(dice_A)
            B_pos += random.choice(dice_B)

            A_steps += 1
            B_steps += 1

        A_steps_list.append(A_steps)
        B_steps_list.append(B_steps)

        # 勝敗判定

        if A_pos >= goal and B_pos >= goal:

            same += 1

        elif A_pos >= goal:

            A_wins += 1

        else:

            B_wins += 1

        # ------------------------------------------
        # 勝率推移用
        # ------------------------------------------

        total_trials = trial + 1

        if calc_mode == "Aの単独勝ちのみ数える":

            current_A = A_wins / total_trials
            current_B = B_wins / total_trials

        elif calc_mode == "同時ゴールを勝ちに含める":

            current_A = (A_wins + same) / total_trials
            current_B = (B_wins + same) / total_trials

        elif calc_mode == "同時ゴールを引き分け扱いにする":

            current_A = A_wins / total_trials
            current_B = B_wins / total_trials

        elif calc_mode == "同時ゴールを除いて計算する":

            effective_trials = total_trials - same

            if effective_trials > 0:

                current_A = A_wins / effective_trials
                current_B = B_wins / effective_trials

            else:

                current_A = 0
                current_B = 0

        A_win_rate_list.append(current_A)
        B_win_rate_list.append(current_B)

    # ==================================================
    # 最終勝率
    # ==================================================

    if calc_mode == "Aの単独勝ちのみ数える":

        A_rate = A_wins / n
        B_rate = B_wins / n

    elif calc_mode == "同時ゴールを勝ちに含める":

        A_rate = (A_wins + same) / n
        B_rate = (B_wins + same) / n

    elif calc_mode == "同時ゴールを引き分け扱いにする":

        A_rate = A_wins / n
        B_rate = B_wins / n
        draw_rate = same / n

    elif calc_mode == "同時ゴールを除いて計算する":

        effective_trials = n - same

        if effective_trials > 0:

            A_rate = A_wins / effective_trials
            B_rate = B_wins / effective_trials

        else:

            A_rate = 0
            B_rate = 0

    # ==================================================
    # 結果表示
    # ==================================================

    st.subheader("結果")

    st.write(f"Aの単独勝ち: {A_wins}")
    st.write(f"Bの単独勝ち: {B_wins}")
    st.write(f"同時ゴール: {same}")

    if calc_mode == "同時ゴールを除いて計算する":
        st.write(f"有効試行回数: {n - same}")

    st.write(f"Aの勝率: {A_rate:.3f}")
    st.write(f"Bの勝率: {B_rate:.3f}")

    if calc_mode == "同時ゴールを引き分け扱いにする":
        st.write(f"引き分け率: {draw_rate:.3f}")

    # ==================================================
    # 4種類の勝率比較
    # ==================================================

    st.subheader("4種類の勝率比較")

    rate_single = A_wins / n

    rate_include = (A_wins + same) / n

    draw_rate_all = same / n

    if n - same > 0:
        rate_exclude = A_wins / (n - same)
    else:
        rate_exclude = 0

    st.write(f"① 単独勝ちのみ : {rate_single:.3f}")

    st.write(f"② 同時ゴールを含む : {rate_include:.3f}")

    st.write(f"③ 引き分け率 : {draw_rate_all:.3f}")

    st.write(f"④ 同時ゴール除外 : {rate_exclude:.3f}")

    # ==================================================
    # 手数分布
    # ==================================================

    if show_steps_graph == "表示する":

        fig, ax = plt.subplots(
            1,
            2,
            figsize=(10, 4)
        )

        ax[0].hist(
            A_steps_list,
            bins=15,
            color="skyblue",
            edgecolor="black"
        )

        ax[0].set_title("サイコロAの手数分布")
        ax[0].set_xlabel("手数")
        ax[0].set_ylabel("度数")

        ax[1].hist(
            B_steps_list,
            bins=15,
            color="orange",
            edgecolor="black"
        )

        ax[1].set_title("サイコロBの手数分布")
        ax[1].set_xlabel("手数")
        ax[1].set_ylabel("度数")

        plt.tight_layout()

        st.pyplot(fig)

    # ==================================================
    # 探究モード：出目分布
    # ==================================================

    if show_distribution:

        st.subheader("出目分布ヒストグラム")

        fig3, ax3 = plt.subplots(
            1,
            2,
            figsize=(10, 4)
        )

        bins_A = range(
            min(dice_A),
            max(dice_A) + 2
        )

        bins_B = range(
            min(dice_B),
            max(dice_B) + 2
        )

        ax3[0].hist(
            dice_A,
            bins=bins_A,
            color="skyblue",
            edgecolor="black",
            align="left"
        )

        ax3[0].set_title("サイコロAの出目分布")
        ax3[0].set_xlabel("出目")
        ax3[0].set_ylabel("個数")

        ax3[1].hist(
            dice_B,
            bins=bins_B,
            color="orange",
            edgecolor="black",
            align="left"
        )

        ax3[1].set_title("サイコロBの出目分布")
        ax3[1].set_xlabel("出目")
        ax3[1].set_ylabel("個数")

        plt.tight_layout()

        st.pyplot(fig3)


    # ==================================================
    # 探究モード：統計量
    # ==================================================

    if show_statistics:

        mean_A = np.mean(dice_A)
        mean_B = np.mean(dice_B)

        var_A = np.var(dice_A)
        var_B = np.var(dice_B)

        std_A = np.std(dice_A)
        std_B = np.std(dice_B)

        st.subheader("サイコロの統計量")

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("### サイコロA")

            st.write(f"期待値：{mean_A:.3f}")
            st.write(f"分散：{var_A:.3f}")
            st.write(f"標準偏差：{std_A:.3f}")

        with col2:

            st.markdown("### サイコロB")

            st.write(f"期待値：{mean_B:.3f}")
            st.write(f"分散：{var_B:.3f}")
            st.write(f"標準偏差：{std_B:.3f}")

        st.subheader("考察のヒント")

        if abs(mean_A - mean_B) < 0.001:

            st.info(
                "AとBの期待値はほぼ同じです。"
                "しかし勝率は同じとは限りません。"
            )

        if var_A > var_B:

            st.success(
                "Aの方が分散が大きく、出目のばらつきが大きいサイコロです。"
            )

        elif var_B > var_A:

            st.success(
                "Bの方が分散が大きく、出目のばらつきが大きいサイコロです。"
            )

        else:

            st.success(
                "AとBの分散はほぼ同じです。"
            )


    # ==================================================
    # 勝率推移グラフ
    # ==================================================

    st.subheader("勝率推移グラフ")

    fig2, ax2 = plt.subplots(figsize=(8, 5))

    ax2.plot(
        A_win_rate_list,
        color="blue",
        linewidth=2,
        label="Aの勝率"
    )

    ax2.plot(
        B_win_rate_list,
        color="red",
        linewidth=2,
        label="Bの勝率"
    )

    ax2.set_title("勝率の試行回数による変化")

    ax2.set_xlabel("試行回数")

    ax2.set_ylabel("勝率")

    ax2.set_ylim(0, 1)

    ax2.grid(True)

    ax2.legend()

    st.pyplot(fig2)





