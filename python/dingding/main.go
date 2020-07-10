/*
@Time    : 2020/7/10
@Author  : Wangcq
@File    : main.go
@Software: GoLand
*/

package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"strings"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/spf13/viper"
)

type message struct {
	Status string `json:"status"`
	Labels struct {
		Alertname string `json:"alertname"`
		Instance  string `json:"instance"`
		Job       string `json:"job"`
		Severity  string `json:"severity"`
	} `json:"labels"`
	Annotations struct {
		Description string `json:"description"`
		Summary     string `json:"summary"`
	} `json:"annotations"`
	StartsAt     string `json:"startsAt"`
	EndsAt       string `json:"endsAt"`
	GeneratorURL string `json:"generatorURL"`
	Fingerprint  string `json:"fingerprint"`
}

type dingding struct {
	Msgtype  string `json:"msgtype"`
	Markdown struct {
		Title string `json:"title"`
		Text  string `json:"text"`
	} `json:"markdown"`
}

func main() {
	initConfig()
	r := gin.Default()
	r.POST("/", httpServer)
	if port := viper.GetString("port"); port != "" {
		panic(r.Run(":" + port))
	}
	panic(r.Run())
}

// http服务
func httpServer(ctx *gin.Context) {
	var d message
	err := ctx.ShouldBindJSON(&d)
	if err != nil {

	}
	d.StartsAt = timeFormat(d.StartsAt)

	if d.Status == "resolved" {
		d.EndsAt = timeFormat(d.EndsAt)
		body := fmt.Sprintf(`#### 监控 
- 告警类型: %s
- 触发时间: %s
- 触发主机: %s
- 告警详情: %s
- 恢复时间: %s
`, d.Labels.Job, d.StartsAt, d.Labels.Instance, d.Annotations.Description, d.EndsAt)
		sendMsg("告警恢复", body)
	} else {
		body := fmt.Sprintf(`####  
- 告警类型: %s
- 触发时间: %s
- 触发主机: %s
- 告警详情: %s
`, d.Labels.Job, d.StartsAt, d.Labels.Instance, d.Annotations.Description)
		sendMsg("告警触发", body)
	}

}

// 发送到钉钉
func sendMsg(tile, text string) {
	webhook := viper.GetString("dingdingurl")
	content := dingding{}
	content.Msgtype = "markdown"
	content.Markdown.Title = tile
	content.Markdown.Text = text
	ctx, _ := json.Marshal(content)
	//创建一个请求
	req, err := http.NewRequest("POST", webhook, strings.NewReader(string(ctx)))
	if err != nil {
		fmt.Println(err)
	}
	client := &http.Client{}
	//设置请求头
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("User-agent", "firefox")
	//发送请求
	resp, err := client.Do(req)
	//关闭请求
	defer resp.Body.Close()
	fmt.Println(resp.StatusCode)
	body, _ := ioutil.ReadAll(resp.Body)
	fmt.Println(string(body))
	if err != nil {
		fmt.Println("handle error")
	}
	if err != nil {
		fmt.Println(err)
	}
}

func timeFormat(t string) string {
	am, _ := time.ParseDuration("1h")
	tt, err := time.Parse("2006-01-02T15:04:05+07:00", t)
	tt = tt.Add(am)
	if err != nil {
		fmt.Println(err)
	}
	return tt.Format("2006-01-02 15:04:05")
}

func initConfig() {
	workDir, _ := os.Getwd()
	viper.SetConfigName("config")
	viper.SetConfigType("yml")
	viper.AddConfigPath(workDir)
	err := viper.ReadInConfig()
	if err != nil {
		panic(err)
	}
}
