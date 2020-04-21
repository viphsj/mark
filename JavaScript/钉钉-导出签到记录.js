// 文件保存可以 试试 https://github.com/eligrey/FileSaver.js
var deptId ={
    "测试1":"88888888",
    "测试2":"66666666"
    };

var taskId;
var xmlHttp;
var deptName;
var fileName;
var fileUrl;

var fromTime = "2020-04-11";
var toTime = "2020-04-17";
//unix 时间戳 毫秒
var fromTimeU = Math.round(new Date(fromTime) / 1);
var toTimeU = Math.round(new Date(toTime) / 1);

function creatXMLHttpRequest() {
    var xmlHttp;
    if (window.ActiveXObject) {
        return xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");
    } else if (window.XMLHttpRequest) {
        return xmlHttp = new XMLHttpRequest();
    }
}

function fu(xmlHttp,url){
    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
                var result = JSON.parse(xmlHttp.responseText);                
                //读取 json 某节点长度，使用 Object.keys().length
                //console.log(Object.keys(result["data"]).length); 
                switch(Object.keys(result["data"]).length){
                    case 5:
                        //读取 id                        
                        taskId = result["data"]["result"];                        
                        //get 下载文件地址
                        main2();                        
                        break;
                    case 2:
                        //progress 到100，就会返回下载文件地址，直接使用
                        if(result["data"]["result"]["progress"] == 100){
                            fileUrl = result["data"]["result"]["url"];
                            console.log(deptName);
                            console.log(fileUrl);                            
                            //fileName = deptName + " 钉钉签到报表 " + fromTime + "-" + toTime + ".xls";                            
                            //console.log(fileName);
                            //saveAs(fileUrl,fileName);
                        } else {
                            //如果 progress 还没有运行到 100，间隔1秒再次请求
                            setTimeout(function(){
                                main2();
                                },1000);                            
                        }
                        break;
                    }
        }
    }
    xmlHttp.open("GET", url, true);
    xmlHttp.send(null);
}

//JavaScript：async/await的基础用法
//https://blog.csdn.net/WuLex/article/details/80713508/
//有了这个async关键字，只是表明里面可能有异步过程，里面可以有await关键字。当然，全部是同步代码也没关系。当然，这时候这个async关键字就显得多余了。不是不能加，而是不应该加。
//async函数，如果里面有异步过程，会等待；
//但是async函数本身会马上返回，不会阻塞当前线程。
//循环 部门id，以便得到 任务id
async function main() { 
    for (key in deptId) {
        deptName = key;
        xmlHttp = creatXMLHttpRequest();    
        var url = "https://attendance.dingtalk.com/attendance/web/export/downloadLocal/asyncDownload.json?fromTime="
            + fromTimeU + "&toTime="
            + toTimeU + "&sendMsg=false&deptId="
            + deptId[key];
        fu(xmlHttp,url);
        await sleep(5000);
    }
}

//使用返回的 任务id 来取 下载文件地址
async function main2() {     
    xmlHttp1 = creatXMLHttpRequest();    
    var url1 = "https://attendance.dingtalk.com/attendance/web/export/downloadLocal/taskProgress.json?taskId="
            + taskId.toString();            
    fu(xmlHttp1,url1); 
    await sleep(5000);
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms))
}

main();
