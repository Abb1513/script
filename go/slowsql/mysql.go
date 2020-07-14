/*
@Time    : 2020/7/13
@Author  : Wangcq
@File    : mysql.go
@Software: GoLand
*/

package main

import (
	"context"
	"fmt"
	_ "github.com/go-sql-driver/mysql"
	"github.com/jinzhu/gorm"
	"github.com/olivere/elastic/v7"
	"time"s
)

type SlowLog struct {
	StartTime time.Time `json:"start_time"`
	UserHost string `json:"user_host"`
	QueryTime string `json:"query_time"`
	LockTime string `json:"lock_time"`
	RowsSent int32 `json:"rows_sent"`
	RowsExamined int32 `json:"rows_examined"`
	Db string `json:"db"`
	LastInsertID int32 `json:"last_insert_id"`
	InsertID int32 `json:"insert_id"`
	ServerID uint32 `json:"server_id"`
	SQLText string `json:"sql_text"`
	ThreadID uint64 `json:"thread_id"`
	Host string `json:"host"`
	Timestamp time.Time `json:"timestamp"`
}


// 获取mysql  慢日志
func GetMysqlSlow(alias , mysqlUrl string)  {
	var slow []SlowLog
 	db, err := gorm.Open("mysql", mysqlUrl)
 	if err != nil {
 		fmt.Println("连接失败, ", err)
	}
 	db.Table("slow_log").Find(&slow)
 	// 没有慢日志则跳过
 	if len(slow) != 0 {
		for _,i := range slow{
			i.Host = alias
			i.Timestamp = time.Now()
			SyncEs(i)
		}
	}
	defer db.Close()
}

// 同步到es
func SyncEs(data SlowLog)  {
	date := time.Now().Format("2006.01.02")
	indexName := "mysql-slowlog-" + date
	servers := []string{"http://192.168.1.96:9200"}
	ctx := context.Background()
	client, err := elastic.NewClient(elastic.SetURL(servers...),elastic.SetBasicAuth("elastic","baoya666"))
	if err != nil {
		fmt.Println("mysql.go, line:61 ", err)
	}
	doc, err := client.Index().
		Index(indexName).
		BodyJson(data).
		Refresh("wait_for").
		Do(ctx)

	if err != nil {
		fmt.Println("mysql.go, line:70 ",err)
	}
	fmt.Printf("Indexed with id=%v, type=%s\n", doc.Id, doc.Type)
}