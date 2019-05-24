<template>
  <div class="main">
    <!-- <h1>Test_Paper_Export</h1> -->
    <!-- 将页面分成两部分 -->
    <div class="demo-split">
      <Split v-model="split">
        <!-- 左侧栏目 -->
        <div slot="left" class="demo-split-pane">
          <!-- 搜索 -->
          <!-- 可拖动列表-题库 -->
          <Scroll style="height:100%">
            <!-- 选择筛选器 -->
            <div class="question-fliter" v-for="(filter, i) in questionFilters" :key="i">
              <strong class="question-fliter-head">{{filter.name}}</strong>
              <div>
                <Button
                  type="info"
                  class="question-fliter-item"
                  @click="e=>{question_fliter(e,i,j)}"
                  v-for="(item, j) in filter.items"
                  :ghost="item.selected"
                  :key="j"
                >{{item.name}}</Button>
              </div>
            </div>
            <!-- 知识点筛选器 -->
            <div class="question-fliter">
              <strong class="question-fliter-head">知识点</strong>
              <div style="padding:10px 0">
                <Tag
                  v-for="item in knowledgepoint_list"
                  :key="item"
                  :name="item"
                  closable
                  @on-close="knowledgepoint_close"
                  style="margin: 3px 5px"
                >{{ item }}</Tag>
              </div>
              <Cascader
                :data="knowledge"
                @on-change="knowledge_point_change"
                transfer
                style=" width: 200px;margin:0 5px"
                change-on-select
                placeholder="请选择知识点标签"
              ></Cascader>
            </div>
            <!-- 学校筛选器 -->
            <div class="question-fliter">
              <strong class="question-fliter-head">学校</strong>
              <Select
                v-model="school_selected"
                multiple
                filterable
                style="min-width: 200px;margin:0 5px;width: auto;"
                placeholder="请输入以搜索学校名称"
                @on-change="school_changed"
              >
                <Option
                  v-for="school in school_list"
                  :value="school.id"
                  :key="school.id"
                >{{school.name}}</Option>
              </Select>
            </div>
            <h2 v-if="questionSearched.length==0">没有查到结果</h2>
            <!-- 左侧拖拽列表 -->
            <draggable v-else v-model="questionSearched" group="question">
              <transition-group>
                <Collapse
                  v-for="element in questionSearched"
                  :key="element.id"
                  class="question-card"
                >
                  <Panel>
                    <div class="question-header" v-html="compiledMarkdown(element.stem,true)"></div>
                    <Icon
                      @click="add(element.id)"
                      style="cursor:pointer"
                      class="add-button"
                      type="md-add"
                    />
                    <!-- <p slot="content" class="question-content">{{element.options}}</p> -->

                    <div
                      v-if="element.type===2|element.type===3|element.type===7|element.type===8"
                      slot="content"
                      class="question-content"
                      v-html="compiledMarkdown(element.options)"
                    ></div>
                    <div slot="content" v-else>
                      <mavon-editor
                        v-model="element.stem"
                        :subfield="false"
                        :defaultOpen="'preview'"
                        :toolbarsFlag="false"
                        :boxShadow="false"
                      />
                    </div>
                    <!-- <div
                      v-else
                      slot="content"
                      class="question-content"
                      v-html="compiledMarkdown(element.stem)"
                    ></div>-->
                  </Panel>
                </Collapse>
              </transition-group>
            </draggable>
          </Scroll>
        </div>
        <!-- 右侧栏目-==================================================================== -->
        <div slot="right" class="demo-split-pane">
          <!-- 可拖动列表-组卷 -->
          <Scroll style="height:100%">
            <div style="display:flex;">
              <Button type="info" style="margin-left:10px" @click="add_detail">加入题型说明</Button>
              <h1 style="flex:1">试卷</h1>
              <Button
                type="success"
                style="margin-right:10px"
                @click="export_paper"
                :loading="export_button_loading"
              >导出试卷</Button>
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
            </div>
            <h2 v-if="questionSelected.length==0" style="padding:20px">还没有题目哦</h2>
            <draggable v-else v-model="questionSelected" group="question">
              <transition-group>
                <Card v-for="element in questionSelected" :key="element.id" class="question-card">
                  <div slot="title" class="question-title">
                    <div class="question-detail" v-html="compiledMarkdown(element.stem,true)"></div>
                    <Icon
                      v-if="element.id>0"
                      @click="remove(element.id)"
                      style="cursor:pointer"
                      class="remove-button"
                      type="md-close"
                    />
                  </div>
                  <p class="question-content">
                    <mavon-editor
                      v-if="element.id>0"
                      v-model="element.stem"
                      :subfield="false"
                      :defaultOpen="'preview'"
                      :toolbarsFlag="false"
                      :boxShadow="false"
                    />
                    <mavon-editor
                      v-model="element.options"
                      :subfield="false"
                      :defaultOpen="'preview'"
                      :toolbarsFlag="false"
                      :boxShadow="false"
                    />
                    <Button
                      v-if="element.id<=0"
                      type="primary"
                      style="float:right;vertical-align: middle;"
                      @click="edit_content(element.id)"
                    >修改</Button>

                    <Modal v-model="showQuestionDetail" width="360" :on-ok="flush_detail">
                      <p slot="header" style="color:#f60;text-align:center">
                        <!-- <Icon type="ios-information-circle"></Icon> -->
                        <span>请输入题型信息</span>
                      </p>
                      <div style="text-align:center">
                        <Form :model="questionDetail" label-position="left" :label-width="100">
                          <FormItem label="题型名">
                            <Input v-model="questionDetail.name"></Input>
                          </FormItem>
                          <FormItem label="题型说明">
                            <Input v-model="questionDetail.detail" type="textarea" :autosize="true"></Input>
                          </FormItem>
                        </Form>
                      </div>
                      <div slot="footer">
                        <Button type="error" size="large" long @click="flush_detail">确定</Button>
                      </div>
                    </Modal>

                    <br>
                    <span v-if="element.id>0" style="color:red">答案：{{element.answer}}</span>
                  </p>
                </Card>
              </transition-group>
            </draggable>
          </Scroll>
        </div>
      </Split>
    </div>
  </div>
</template>

<script>
import draggable from "vuedraggable";
import marked from "marked";
import { mavonEditor } from "mavon-editor";
export default {
  name: "Test_Paper_Export_Mode",
  data() {
    return {
      showDownloadPage: false,
      showQuestionDetail: false,
      question_now_id: 0,
      questionDetail: {
        name: "",
        detail: ""
      },
      randomKey: "",
      questionSearched: [
        {
          id: 0,
          stem: "xswl",
          options:
            "我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容"
        }
      ],
      questionSelected: [
        {
          id: 0,
          stem: "title",
          options: "试卷说明"
        }
      ],
      split: 0.5,
      // 筛选题库
      questionFilters: [
        {
          name: "难度",
          items: [
            { name: "困难", selected: true },
            { name: "中等", selected: true },
            { name: "简单", selected: true },
            { name: "智障", selected: true },
            { name: "沙雕", selected: true }
          ]
        },
        {
          name: "题型",
          items: [
            { name: "填空", selected: true },
            { name: "选择", selected: true },
            { name: "判断", selected: true },
            { name: "bulabula", selected: true }
          ]
        }
      ],
      knowledgepoint_list: [], // 已选择的知识点列表
      knowledge: [], // 全部的知识点列表
      paperInfo: { ok: false },
      school_selected: [], //已经选择的学校
      school_list: [
        { name: "上海中学", id: 1 },
        { name: "复旦附中", id: 2 },
        { name: "上大附中", id: 3 }
      ], ///已经有的学校
      export_button_loading: false,
      type_id: -1
    };
  },
  mounted() {
    let that = this;
    //  获取知识点列表
    console.log("params:", this.$route.params);
    this.paperInfo = {
      paper_name: "兰生复旦7年级综合卷",
      subject: 2,
      grade: 6,
      ok: true
    };
    console.log("this.$route.params", this.$route.params);
    if (Object.keys(this.$route.params).length)
      this.paperInfo = this.$route.params;
    this.questionSelected[0].stem = this.paperInfo.paper_name;
    this.paperInfo.ok = true;
    $.ajax({
      url: that.$site + "api/query_knowledgepoint",
      dataType: "json",
      data: {
        subject: this.paperInfo.subject,
        id: true
      },
      success: function(data) {
        // console.log(data);
        that.knowledge = [];
        for (var i = 0; i < data.length; i++) {
          that.knowledge.push(data[i]);
        }
      }
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
              name: element.name,
              selected: true
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
              name: element.name,
              selected: true
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

    // 查询学校信息
    this.$axios
      .get(this.$site + "api/query_school")
      .then(res => {
        console.log("query_school", res.data);
        var schools = [];
        for (const item in res.data) {
          if (res.data.hasOwnProperty(item)) {
            const element = res.data[item];
            schools.push({
              id: element.id,
              name: element.name,
              selected: true
            });
          }
        }
        this.school_list = schools;
      })
      .catch(err => {
        this.$Notice.error({
          title: "查询学校失败",
          desc: err
        });
      });
    this.flush_questions(true);
    this.randomKey = this.randomNum();
  },
  computed: {},
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
    flush_detail() {
      var question_now = this.questionSelected.find(q => {
        return this.question_now_id === q.id;
      });
      question_now.stem = this.questionDetail.name;
      question_now.options = this.questionDetail.detail;
      this.showQuestionDetail = false;
    },
    get_first(context) {
      return context;
    },
    add_detail() {
      this.questionSelected.push({
        id: this.type_id,
        stem: "选择题",
        options: "题型说明"
      });
      this.type_id -= 1;
    },
    edit_content(id) {
      this.question_now_id = id;
      var question_now = this.questionSelected.find(q => {
        return this.question_now_id === q.id;
      });
      this.questionDetail.name = question_now.stem;
      this.questionDetail.detail = question_now.options;
      this.showQuestionDetail = true;
      // todo 修改content
    },
    test() {
      let that = this;
      console.log("恭喜你进入测试程序");
    },
    export_paper() {
      this.export_button_loading = true;
      this.$axios
        .post(this.$site + "api/paper_export", {
          questionSelected: this.questionSelected,
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
              title: "导出失败"
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
    },
    flush_questions(isall = false) {
      console.log("更新问题");
      var datas = {
        paperInfo: this.paperInfo,
        filters: this.questionFilters,
        knowledge_point: this.knowledgepoint_list,
        school_selected: this.school_selected
      };
      if (isall) datas = { isall: true };
      this.$axios
        .post(this.$site + "api/search_question", datas)
        .then(res => {
          var ok = res.data.ok;
          if (ok) {
            this.questionSearched = res.data.data;
            // for (let i = 0; i < res.data.data.length; i++) {
            //   const e = res.data.data[i];
            //   this.questionSearched
            // }
            this.$Notice.success({
              title: "查找成功",
              desc: "不写点什么感觉过意不去呢"
            });
            console.log(res.data);
          } else {
            this.$Notice.error({
              title: "查找失败",
              desc: "不写点什么感觉过意不去呢"
            });
          }
        })
        .catch(err => {
          this.$Notice.error({
            title: "查找失败",
            desc: err
          });
        });
    },
    // 拖拽列表的添加和删除事件
    add(id) {
      this.questionSearched.forEach((item, index, arr) => {
        if (item.id === id) {
          this.questionSelected.push(item);
          arr.splice(index, 1);
        }
      });
    },
    remove(id) {
      this.questionSelected.forEach((item, index, arr) => {
        if (item.id === id) {
          this.questionSearched.push(item);
          arr.splice(index, 1);
        }
      });
    },
    question_fliter(e, i, j) {
      // console.log(e, i, j);
      this.flush_questions();
      this.questionFilters[i].items[j].selected = !this.questionFilters[i]
        .items[j].selected;
    },
    school_changed() {
      console.log("学校变了呢");
      this.flush_questions();
    },
    // 知识点级联选择变化触发的事件
    knowledge_point_change(value, selectedData) {
      // console.log("触发级联选择器change事件");
      this.flush_questions();
      if (this.knowledgepoint_list.indexOf(value[value.length - 1]) === -1) {
        this.knowledgepoint_list.push(value[value.length - 1]);
      }
    },
    // 关闭知识点标签触发的事件
    knowledgepoint_close(event, name) {
      const index = this.knowledgepoint_list.indexOf(name);
      this.knowledgepoint_list.splice(index, 1);
      this.flush_questions();
    }
  },
  watch: {
    questionFilters() {
      console.log("questionFilters has changed", this.questionFilters);
    }
  },
  computed: {
    compiledMarkdown() {
      return (context, first = false) => {
        if (first) {
          if (context.length > 20) {
            return marked(context.substr(0, 20) + "...", { sanitize: true });
          }
        }
        return marked(context, { sanitize: true });
      };
    }
  },
  components: {
    draggable
  }
};
</script>

<style scope>
.demo-split {
  /* height: 800px; */
  border: 1px solid #dcdee2;
}

.demo-split-pane {
  padding: 10px;
}

.question-card {
  margin: 10px;
}

.question-title {
  text-align: left;
  display: flex;
  width: 100%;
}

.question-content {
  text-align: left;
  display: flow-root;
}

.ivu-card-head {
  display: flex;
}

.add-button {
  float: right;

  font-size: 20px;
  margin-top: 2px;
}

.remove-button {
  line-height: 20px;
  float: right;
}

.ivu-collapse-item {
  text-align: left;
}

.question-content {
  font-size: 14px;
}

.ivu-collapse-content-box {
  font-size: 12px;
}

.demo-split-pane {
  height: 100%;
}

.ivu-scroll-container {
  height: 98% !important;
}

#app,
html,
body,
.main,
.demo-split {
  height: 100%;
}
.ivu-layout-content {
  height: fit-content;
}
.question-fliter-head {
  font-size: 13px;
  margin: 10px 20px;
  min-width: 40px;
}
.question-fliter-item {
  margin: 2px 5px;
  float: left;
}
.question-fliter {
  display: flex;
  align-items: center;
}
.ivu-layout {
  background: #fff;
}
/* 搞定左边的显示 */
.ivu-collapse-header {
  font-size: 17px;
  display: flex;
  align-items: center;
  padding-left: 10px;
}
.question-header {
  flex: 1;
}
.v-note-wrapper {
  min-width: 0 !important;
  min-height: 0 !important;
}
.v-note-wrapper .v-note-panel .v-note-show .v-show-content {
  background: #fff !important;
}
.v-note-wrapper .v-note-panel {
  border: 0px !important;
}
.question-detail {
  flex: 1;
}
.v-note-wrapper {
  z-index: 20 !important;
}
.back-ground {
  background: #c9ccd3;
  background-image: linear-gradient(
    -180deg,
    rgba(255, 255, 255, 0.5) 0%,
    rgba(0, 0, 0, 0.5) 100%
  );
  background-blend-mode: lighten;
}

.vertical-center-modal {
  display: flex;
  align-items: center;
  justify-content: center;
}
.ivu-modal {
  position: unset;
}
</style>
