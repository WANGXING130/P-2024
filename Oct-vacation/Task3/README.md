# Task 3

请补充个人信息后，在此完成报告！

代码如下：
```
function calculate(expression) {

  const numberStack = [];
  const operatorStack = [];
  
  const operators = {
    "+": (a, b) => a + b, 
    "-": (a, b) => a - b,
    "*": (a, b) => a * b,
    "/": (a, b) => a / b, 
    "^": (a, b) => Math.pow(a,b),
    "sin": (x)  => Math.sin(x *Math.PI / 180),
    "cos": (x)  => Math.cos(x *Math.PI / 180),
    "tan": (x)  => Math.tan(x *Math.PI / 180)
  };

  const precedence = {
    "+": 1, 
    "-": 1,
    "*": 2, 
    "/": 2,
    "^": 3,
    "sin": 3,
    "cos": 3,
    "tan": 3,
  };

  // applyOperator 函数用于执行具体的运算操作
  function applyOperator(oper, second, first) {
    if (["sin","cos","tan"].includes(oper)) {            //sin cos tan
      return operators[oper](first);
    } else {
    return operators[oper](first, second);               //+-*/^
    }       
  }

  // greaterPrecedence 函数用于比较两个操作符的优先级
  function greaterPrecedence(op1, op2) {
    return precedence[op1] >= precedence[op2];
  }

  // evaluate 函数用于执行栈中的所有操作
  function evaluate() { 
    while (operatorStack.length > 0) {
      const first = numberStack.pop();
      const second = numberStack.pop();
      const oper = operatorStack.pop();
      numberStack.push(applyOperator(oper, first, second));
    }
    // 返回最终的计算结果
    return numberStack.pop();
  }

  // 使用正则表达式将输入的表达式分割成操作数和操作符
 
  const tokens = expression.match(/(\d+(\.\d+)?)|([\+\-\*\/\^\(\)])|(sin|cos|tan)/g);

  // 遍历分割后的每个 token
  for (const token of tokens) {

    if (!isNaN(token)) {             
      numberStack.push(parseFloat(token));
    } else if (["+", "-", "*", "/","^","sin","cos","tan"].includes(token)) {

      while (
        operatorStack.length > 0 &&
        greaterPrecedence(operatorStack[operatorStack.length - 1], token)
      ) {
        numberStack.push(
          applyOperator(
            operatorStack.pop(),
            numberStack.pop(),
            numberStack.pop()
          )
        );
      }
      // 将当前操作符压入符号栈
      operatorStack.push(token);
    } else if (token == "(") {                                     //栈顶为（时，前面若有也已运算完毕
      operatorStack.push(token);
    } else if (token == ")") {
      while (operatorStack[operatorStack.length - 1] != "(")       //逻辑同括号外
      {
        numberStack.push(
          applyOperator(
            operatorStack.pop(),
            numberStack.pop(),
            numberStack.pop()
          )                          
        );
      }
      operatorStack.pop();                                         //去掉（

    }
  }
  // 调用 evaluate 函数计算最终结果并返回
  return evaluate();
}

// 使用示例
const result = calculate("(3.5+0.5)*2-1+sin(90)");
console.log(result); // 输出计算结果
```

注： 
     1. 完成的添加幂函数 括号 三角函数那块 、 kfc架构复现工程 和躺平
     2. 实在搞不定三角函数啊，expression中去掉三角函数，（）、幂运算一切正常，否则NaN

问题：

将括号弹进符号栈时，使用了两个operatorStack.pop(),以为可以弹出（），实际上检测到）时根本没有压进


@Author:  王兴
@Email:   243286054@qq.com
