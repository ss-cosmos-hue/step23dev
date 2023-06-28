# 概要
# fit level(best fit, worst fit)
first fit
best fit
worst fit 実装
# 結果
## first fit
![firstfit without bin](firstfit_without_bin.png)
## best fit
![bestfit without bin](bestfit_without_bin.png)
- utiizationは全体的に増加している
- 時間効率は、challenge 1,2,3では変わらないか増加しているが、challenge4,5では減少している。
- 隙間が空いているので、再度mallocを回す必要がないからかもしれない。
## worst fit
![worstfit without bin](worstfit_without_bin.png)


# free list bin
![bestfit with bin](bestfit_free_list_bin.png)
単純なbestfitの実装より、時間効率が良い。
# 