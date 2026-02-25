# 하위 호환성 유지: portal/wiki/book → portal/wiki/struct/book
# 새로운 코드에서는 wiz.model("portal/wiki/struct").book 사용을 권장합니다.
Model = wiz.model("portal/wiki/struct/book")
