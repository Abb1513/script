/*
@Time    : 2020/7/13
@Author  : Wangcq
@File    : main.go.go
@Software: GoLand
*/

package main

import (
	"github.com/spf13/viper"
	"os"
	"time"
)


func main()  {
	InitConfig()
	mysqlHost := viper.GetStringSlice("mysqlurl")
	for {
		// 阿里云每分钟会收集一次慢日志， 并清空表 58s 运行 预留2s 程序运行时间
		date := time.Now().Second()
		if date == 58{
			for _, i := range  mysqlHost {
				mysqlUrl := viper.GetString(i)
				GetMysqlSlow(i, mysqlUrl)
			}
		}

	}

}

func InitConfig()  {
	workDir, _ := os.Getwd()
	viper.SetConfigName("config")
	viper.SetConfigType("yml")
	viper.AddConfigPath(workDir)
	err := viper.ReadInConfig()
	if err != nil {
		panic(err)
	}
}