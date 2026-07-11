# Trace — 주식 학습 로드맵 (중장기 목돈)

- run-id: 2026-07-11_stocks-learning-roadmap
- goal: 주식을 아무것도 모르는 상태에서 중장기 목돈 만들기 목적으로 학습하도록 돕기
- box in force: 모든 축 허용, max_depth 3, max_breadth 6, max_rounds 3,
  "one-line goal stays one line"
- operator bias applied: OPERATOR.md v0.3 (anti-waste, iterative-first,
  fidelity-by-slack, no over-decomposition, revisit-hook on every stop)

## 자기설계 (four questions)

- **Order?** 예. 기초→자산→전략→계좌·세금→실행→반복은 진짜 의존관계
  (기초 없이 실행하면 손해). → order 축 오픈, 6단계 line.
- **Breadth?** 예. 학습 주제가 서로 독립된 6개 기둥으로 분리(병렬 학습 가능).
  max_breadth 6 이내. → breadth 오픈.
- **Depth?** 제한적. '전략' 기둥만 한 겹 더 확장(적립식/자산배분/저비용/리밸런싱/
  buy&hold). 나머지는 초보 1차 패스라 얕게 — 과잉분해 억제(operator '낭비' 회피).
  → depth 1레벨만.
- **Time?** 중심. 주제(투자)도 학습도 반복 게임. one-shot 완벽 대신 v1 1차 패스를
  내보내고 심화는 다음 라운드로. → time 축 프레이밍, 라운드1 산출.

## 스톱 조건 / 되돌아볼 고리

- depth: '전략' 1레벨에서 정지(초보에게 충분).
- time: 라운드1에서 정지, 단 output.md의 "다음 라운드에 깊게 팔 것"이 revisit hook.
  (operator 규칙: 모든 time-stop은 다시 볼 고리를 남긴다.)

## 열린 축 요약

order + breadth + depth(1) — 시간축 라운드1 산출물. 개별 종목 추천/투자자문은
범위 밖(교육 원리만). 산출: output.md.
