### 图方便，备份本地数据库备份文件到ftp服务器，文件存储成 bat，定时运行就可以。
```batch
@echo off
echo.
set data=%date:~0,4%_%date:~5,2%_%date:~8,2%
echo open XXX.XXX.XXX.XXX 667 >ftp.txt
echo ftpuser>>ftp.txt
echo ftppassword>>ftp.txt
echo binary>>ftp.txt
echo cd ftp服务器文件夹>>ftp.txt
echo lcd 本地文件夹>>ftp.txt
echo prompt>>ftp.txt
echo mput xxxxxx_%data%*.* >>ftp.txt
echo close>>ftp.txt
echo bye>>ftp.txt
ftp.exe -s:ftp.txt
echo.
```
