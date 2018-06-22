baseUrl = "http://app1.sfda.gov.cn/datasearch/face3/"
filename = "domestic.csv"

total_num = 166112
# total_pager = 11075
total_pager = 20
first_pager = 1
step = 4

"""
<form method="post" id="pageForm" name="pageForm" action="search.jsp">
<input type="hidden" name="tableId" value="25">
<input type="hidden" name="bcId" value="124356560303886909015737447882">
<input type="hidden" name="curstart" value="">
<input type="hidden" name="tableName" value="TABLE25">
<input type="hidden" name="viewtitleName" value="COLUMN167">
<input type="hidden" name="viewsubTitleName" value="COLUMN821,COLUMN170,COLUMN166">
<input type="hidden" name="keyword" value="">
<input type="hidden" name="tableView" value="国产药品">
<input type="hidden" name="cid" value="0">
<input type="hidden" name="ytableId" value="0">
<input type="hidden" name="searchType" value="search">
</form>
"""

def get_all_pager_url(index):
    return baseUrl + "search.jsp?" \
           + "tableId=25&State=1" \
           + "&bcId=124356560303886909015737447882&State=1" \
           + "&curstart=" + str(index) +"&State=1"\
           + "&tableName=TABLE25&State=1"\
           + "&viewtitleName=COLUMN167&State=1"\
           + "&viewsubTitleName=COLUMN821,COLUMN170,COLUMN166&State=1" \
           + "&tableView=国产药品&State=1" \
           + "&cid=0&State=1" \
           + "&ytableId=0&State=1"\
           + "&searchType=search&State=1"
