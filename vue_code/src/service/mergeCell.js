let colNumArray = [];   // 每一列需要合并的行数数组
let colPosIndexArray = [];   // 记录需要合并的列的位置

/**
 * 数据初始化
 * @param {需要合并的列数，即 字段名数组的长度 colNameArrayParam.length} colNum
 */
function initMerge(colNum) {
  console.log(11111111, colNum)
  colNumArray = []
  colPosIndexArray = []
  for (let i = 0; i < colNum; i++) {
    colNumArray.push([1]); // 初始化第一行
    colPosIndexArray.push([0]);
  }
}

/**
 * 合并处理
 * @param {需要合并的字段名数组} colNameArrayParam
 * @param {用来合并的源数据} dataParam
 */
const colNumberMergeCount = function (colNameArrayParam, dataParam) {
  // var dataParam = 111111111
  for (let i = 0; i < dataParam.length; i++) { //遍历每一条数据
    if (i == 0) {
      initMerge(colNameArrayParam.length);  //初始化第一行
    } else {
      let isAnd = true; // 记录必须前面的列合并才能合并当前列 如第3列合并  必须第1、2列也要合并
      for (let j = 0; j < colNameArrayParam.length; j++) { //遍历需要合并的列，计算合并的行数
        if (isAnd && dataParam[i][colNameArrayParam[j]] === dataParam[i - 1][colNameArrayParam[j]]) {  //判断是否和上一列内容相同
          colNumArray[j][colPosIndexArray[j]] += 1; // 如相同 则+1 表示合并的行数，
          colNumArray[j].push(0);  // 再push新的一行为0，表示这一行被合并
          // isAnd = true;  // 记录并且关系
        } else {
          isAnd = false; // 如果不相同，刚之后的全都不合并
          colNumArray[j].push(1);  //push新行 默认为1
          colPosIndexArray[j] = i; //更新计算合并行数的位置，如 从第1行开始计算，如果一直相同位置不变，后面一直push新行为0，反之，没有合并刚更新位置+1，从下一行开始计算合并
        }
      }
    }
  }
  console.log(colNumArray)
  return colNumArray;  //返回合并处理后的数据
}

/**
 * 合并函数  绑定表格上的span-method函数 (暂未使用，该函数使用的页面内部实现)
 * @param {span-method 回调参数} param0
 */
function spanMethod({row, column, rowIndex, columnIndex}) {
  const _row = colNumArray[columnIndex][rowIndex];
  const _col = _row > 0 ? 1 : 0; //如果被合并了_row=0则它这个列需要取消
  return {
    rowspan: _row,
    colspan: _col
  };
}

export default colNumberMergeCount;
