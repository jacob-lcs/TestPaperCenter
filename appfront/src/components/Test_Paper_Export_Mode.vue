<template>
  <div class="export_all">
    <Row type="flex">
      <!-- 轮播图 -->
      <Col span="12" offset="2" style="margin-top: 60px">
        <Carousel autoplay :autoplay-speed="2500" loop>
          <CarouselItem>
            <div class="demo-carousel1" style="color: white "></div>
          </CarouselItem>
          <CarouselItem>
            <div class="demo-carousel2"></div>
          </CarouselItem>
          <CarouselItem>
            <div class="demo-carousel3"></div>
          </CarouselItem>
        </Carousel>
      </Col>
      <!-- 入口按钮 -->
      <Col span="7" offset="2" style="margin-top: 100px">
        <Card class="card-button">
          <div style="text-align:center" @click="export_byhands">
            <Icon size="100" type="md-hand" style="margin-top: -20px"/>
            <h3>手动组卷</h3>
          </div>
        </Card>

        <Card class="card-button" style="margin-top: 80px">
          <div style="text-align:center" @click="export_auto">
            <Icon size="100" type="md-color-wand" style="margin-top: -20px"/>
            <h3>自动组卷</h3>
          </div>
        </Card>
      </Col>
    </Row>
    <!-- 信息填写框！ -->
    <Modal v-model="showPaperInfo" :width="modal_width" class-name="vertical-center-modal">
      <p slot="header" style="text-align:center">
        <span>请输入试卷信息</span>
      </p>
      <div style="display:flex;">
        <!-- 基本信息 -->
        <div
          style="text-align:center;border-right: 1px solid rgba(0, 0, 0, 0.13);padding-right: 15px;"
        >
          <Form :model="paperInfo" label-position="left" :label-width="70">
            <FormItem label="试卷抬头">
              <Input v-model="paperInfo.paper_name"></Input>
            </FormItem>
            <FormItem label="科目">
              <Select v-model="paperInfo.subject" @on-change="flush_subject">
                <Option
                  v-for="subject in subjects"
                  :value="subject.id"
                  :key="subject.id"
                >{{subject.name}}</Option>
              </Select>
            </FormItem>
            <FormItem label="年级" style="margin-bottom:0px">
              <Select v-model="paperInfo.grade">
                <Option v-for="grade in grades" :value="grade.id" :key="grade.id">{{grade.name}}</Option>
              </Select>
            </FormItem>
          </Form>
        </div>
        <!-- 自动组卷题型信息 -->
        <div style="display:flex;flex-direction:column" v-if="mode=='auto'">
          <div
            style="padding:0 10px;display:flex;margin-bottom:10px;align-items: center;"
            v-for="(item, i) in questionInfo"
            :key="i"
          >
            <Select placeholder="题型" class="paper-info-selecter" v-model="item.type">
              <Option
                v-for="(type, j) in questionFilters[1].items"
                :value="type.id"
                :key="j"
              >{{type.name}}</Option>
            </Select>
            <Select placeholder="难度" class="paper-info-selecter" v-model="item.difficulty">
              <Option
                v-for="(diff, j) in questionFilters[0].items"
                :value="diff.id"
                :key="j"
              >{{diff.name}}</Option>
            </Select>
            <Input v-model="item.score" class="paper-info-selecter" placeholder="分值" type="number"></Input>
            <Input v-model="item.num" class="paper-info-selecter" placeholder="数量" type="number"></Input>
            <Icon
              @click="remove(i)"
              size="20"
              style="cursor:pointer;"
              class="remove-button"
              type="md-close"
            />
          </div>
          <div style="padding:0 10px;display:flex;align-items: center;justify-content: flex-end;">
            <Button style="min-width: 100px;margin-right:7px" type="error">总分:{{sum_score}}</Button>
            <Button type="primary" style="min-width: 100px;" @click="add">添加</Button>
          </div>
        </div>
      </div>

      <div slot="footer">
        <Button
          type="primary"
          size="large"
          long
          :loading="export_button_loading"
          @click="confirm"
        >确定</Button>
      </div>
    </Modal>
    <Modal v-model="showDownloadPage" class-name="vertical-center-modal">
      <p slot="header" style="font-size:20px">请选择导出方式</p>

      <div style="text-align:center;">
        <Button type="primary" class="download-button" @click="download(1)">
          仅导出试题
          <br>不包含答案
        </Button>
        <Button type="primary" class="download-button" @click="download(2)">
          导出试题
          <br>包含答案
        </Button>
        <Button type="primary" class="download-button" @click="download(3)">
          导出试题压缩包
          <br>含答案和不含答案版本
        </Button>
      </div>
      <div slot="footer"></div>
    </Modal>
    <!-- </Row> -->
  </div>
</template>

<script>
export default {
  name: "Test_Paper_Export_Mode",
  data() {
    return {
      showPaperInfo: false,
      showDownloadPage: false,
      export_button_loading: false,
      paperInfo: {
        paper_name: "兰生复旦7年级综合卷",
        // school: "复旦什么学校",
        subject: 2,
        grade: 6
      },
      modal_loading: false,
      randomKey: "ASDS23F3",
      mode: "auto",
      subjects: [
        { id: 1, name: "语文", selected: true },
        { id: 2, name: "数学", selected: true },
        { id: 3, name: "英语", selected: true },
        { id: 4, name: "政治", selected: true },
        { id: 5, name: "历史", selected: true },
        { id: 6, name: "地理", selected: true },
        { id: 7, name: "物理", selected: true },
        { id: 8, name: "化学", selected: true },
        { id: 9, name: "生物", selected: true }
      ],
      grades: [
        { id: 1, name: "一年级", selected: true },
        { id: 2, name: "二年级", selected: true },
        { id: 3, name: "三年级", selected: true },
        { id: 4, name: "四年级", selected: true },
        { id: 5, name: "五年级", selected: true },
        { id: 6, name: "六年级", selected: true },
        { id: 7, name: "七年级", selected: true },
        { id: 8, name: "八年级", selected: true },
        { id: 9, name: "九年级", selected: true }
      ],
      questionInfo: [
        {
          type: 21,
          difficulty: 3,
          score: 7,
          num: 3
        },
        {
          type: 33,
          difficulty: 2,
          score: 6,
          num: 4
        },
        {
          type: 23,
          difficulty: 1,
          score: 1,
          num: 2
        }
      ],

      questionFilters: [
        {
          name: "难度",
          items: [{ name: "沙雕", selected: true, id: 1 }]
        },
        {
          name: "题型",
          items: [{ name: "填空", selected: true, id: 1 }]
        }
      ]
    };
  },
  mounted() {
    // 路径保护
      if (sessionStorage.getItem('per_name') === null || sessionStorage.getItem('identity') === 'keyboarder') {
        this.$router.push("/")
      } else {
        console.log(sessionStorage.getItem('per_name'))
      }
    // 查询学科
    this.$axios
      .get(this.$site + "api/query_subjects")
      .then(res => {
        console.log("query_subjects", res.data);
        var subjects = [];
        for (const item in res.data) {
          if (res.data.hasOwnProperty(item)) {
            const element = res.data[item];
            subjects.push({
              id: element.id,
              name: element.name,
              selected: true
            });
          }
        }
        this.subjects = subjects;
      })
      .catch(err => {
        this.$Notice.error({
          title: "查询题型失败",
          desc: err
        });
      });
    // 查询年级
    this.$axios
      .get(this.$site + "api/query_grades")
      .then(res => {
        console.log("query_grades", res.data);
        var grades = [];
        for (const item in res.data) {
          if (res.data.hasOwnProperty(item)) {
            const element = res.data[item];
            grades.push({
              id: element.id,
              name: element.name,
              selected: true
            });
          }
        }
        this.grades = grades;
      })
      .catch(err => {
        this.$Notice.error({
          title: "查询年级失败",
          desc: err
        });
      });
    // 查询难度信息
    this.$axios
      .get(this.$site + "api/query_difficulty")
      .then(res => {
        // console.log("query_difficulty", res.data);
        var difficulties = [];
        for (const item in res.data) {
          if (res.data.hasOwnProperty(item)) {
            const element = res.data[item];
            difficulties.push({
              id: element.id,
              name: element.name
            });
          }
        }
        this.questionFilters[0]["items"] = difficulties;
      })
      .catch(err => {
        this.$Notice.error({
          title: "查询难度信息失败",
          desc: err
        });
      });

    // 查询题型
    this.$axios
      .get(this.$site + "api/query_types", {
        params: { subject: this.paperInfo.subject, id: true }
      })
      .then(res => {
        console.log("query_types", res.data);
        var difficulties = [];
        for (const item in res.data) {
          if (res.data.hasOwnProperty(item)) {
            const element = res.data[item];
            difficulties.push({
              id: element.id,
              name: element.name
            });
          }
        }
        this.questionFilters[1]["items"] = difficulties;
      })
      .catch(err => {
        this.$Notice.error({
          title: "查询题型失败",
          desc: err
        });
      });
    this.randomKey = this.randomNum();
  },
  methods: {
    randomNum() {
      var a = [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9"
      ];
      var i = 0;
      var res = "";
      while (i < 8) {
        res += a[parseInt(Math.random() * 35, 10)];
        i += 1;
      }
      return res;
    },

    download(n) {
      switch (n) {
        case 1:
          window.open(
            this.$site +
              "static/TestPaperManager/docx/" +
              this.randomKey +
              "/" +
              this.randomKey +
              ".docx"
          );
          break;
        case 2:
          window.open(
            this.$site +
              "static/TestPaperManager/docx/" +
              this.randomKey +
              "/" +
              this.randomKey +
              "answer.docx"
          );
          break;
        case 3:
          window.open(
            this.$site +
              "static/TestPaperManager/zip/" +
              this.randomKey +
              ".zip"
          );
          break;
      }
    },
    remove(id) {
      this.questionInfo.splice(id, 1);
    },
    flush_subject() {
      // 查询题型
      this.$axios
        .get(this.$site + "api/query_types", {
          params: { subject: this.paperInfo.subject, id: true }
        })
        .then(res => {
          console.log("query_types", res.data);
          var difficulties = [];
          for (const item in res.data) {
            if (res.data.hasOwnProperty(item)) {
              const element = res.data[item];
              difficulties.push({
                id: element.id,
                name: element.name
              });
            }
          }
          this.questionFilters[1]["items"] = difficulties;
        })
        .catch(err => {
          this.$Notice.error({
            title: "更新题型信息失败Rua",
            desc: err
          });
        });
    },
    export_byhands() {
      console.log("manual");
      this.mode = "manual";
      this.showPaperInfo = true;
    },
    export_auto() {
      console.log("auto");
      this.mode = "auto";
      this.showPaperInfo = true;
    },
    form_valid() {
      var ok = false;
      let that = this;
      for (let i = 0; i < this.questionInfo.length; i++) {
        const q = this.questionInfo[i];
        if (q.num != undefined && q.num != 0) {
          if (q.score != undefined && q.score != 0) {
            ok = true;
          }
          if (q.score == undefined || q.score == 0) {
            that.$Notice.error({
              title: "好像有的题目分值还没填鸭~",
              desc: "不填分值的话我们也很难办呢！"
            });
            return false;
          }
          if (
            this.questionFilters[0].items.findIndex(e => {
              return e.id == q.difficulty;
            }) === -1
          ) {
            that.$Notice.error({
              title: "有的题目难度还没选择哦",
              desc: "不选择难度我们也很难组卷的哦~亲~"
            });
            return false;
          }
          if (
            this.questionFilters[1].items.findIndex(e => {
              return e.id == q.type;
            }) === -1
          ) {
            that.$Notice.error({
              title: "有的题目类型还没选择哦",
              desc: "不选择题型我们也很难组卷的哦~亲~"
            });
            return false;
          }
        }
      }
      if (!ok) {
        that.$Notice.error({
          title: "一道题都还没有呢~添加几道吧~",
          desc: "一道题也没有我们不会导出空试卷的哦~亲~"
        });
      }
      return ok;
    },
    confirm() {
      if (this.mode === "manual")
        this.$router.push({
          name: "Test_Paper_Export_Byhands",
          params: this.paperInfo
        });
      else {
        // 表单校验
        if (this.form_valid()) {
          // 导出api
          console.log("表单验证成功呢");
          this.export_button_loading = true;
          this.$axios
            .post(this.$site + "api/auto_export", {
              questionInfo: this.questionInfo,
              paperInfo: this.paperInfo,
              randomKey: this.randomKey
            })
            .then(res => {
              console.log(res);
              if (res.data.ok) {
                this.$Notice.success({
                  title: "导出成功"
                });
                this.export_button_loading = false;
                this.showDownloadPage = true;
              } else {
                this.$Notice.error({
                  title: "导出失败",
                  desc: res.data.errmsg
                });
                this.export_button_loading = false;
              }
            })
            .catch(err => {
              console.log(err);
              this.$Notice.error({
                title: "导出失败",
                desc: err
              });
              this.export_button_loading = false;
            });
        }
      }
    },
    add() {
      this.questionInfo.push({
        type: 0,
        difficulty: 0,
        score: 0,
        num: 0
      });
    }
  },
  computed: {
    sum_score() {
      var sum = 0;
      for (let i = 0; i < this.questionInfo.length; i++) {
        const e = this.questionInfo[i];
        sum += parseInt(e.score) * parseInt(e.num);
      }
      return sum;
    },
    modal_width() {
      if (this.mode === "auto") {
        return 800;
      } else {
        return 300;
      }
    }
  }
};
</script>

<style scope>
.export_all {
  background-image: url("../assets/img/box.png");
  background-repeat: no-repeat;
  background-size: 100% 100%;
  background-attachment: fixed;
  height: 100%;
}

.demo-carousel1 {
  height: 500px;
  background-image: url("../assets/img/teacher.jpg");
  background-size: 50vw auto;
}

.demo-carousel2 {
  height: 500px;
  background-image: url("../assets/img/boy.jpg");
  background-size: 50vw auto;
}

.demo-carousel3 {
  height: 500px;
  background-image: url("../assets/img/classroom.jpg");
  background-size: 50vw auto;
}

.card-button {
  background-color: rgba(255, 255, 255, 0.4);
  width: 320px;
  height: 160px;
  cursor: pointer;
  padding: 30px;
  margin-top: 0px;
}

.ivu-layout-content {
  height: fit-content;
}
.paper-info-selecter {
  min-width: 100px;
  padding: 0 5px;
}
.download-button {
  font-size: 12px;
  margin: 17px;
  padding: 20px;
}
/* .ivu-layout-content {
    position: absolute;
    top: 50px;
    bottom: 0;
    left: 0;
    width: 100%;
  } */
.vertical-center-modal {
  display: flex;
  align-items: center;
  justify-content: center;
}
.ivu-modal {
  top: 0;
}
</style>

