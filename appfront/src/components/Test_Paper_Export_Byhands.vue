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
              >
                <Option
                  v-for="school in school_list"
                  :value="school.id"
                  :key="school.id"
                >{{school.name}}</Option>
              </Select>
            </div>
            <draggable v-model="questionSearched" group="question">
              <transition-group>
                <Collapse
                  v-for="element in questionSearched"
                  :key="element.id"
                  class="question-card"
                >
                  <Panel>
                    {{element.name}}
                    <Icon
                      @click="add(element.id)"
                      style="cursor:pointer"
                      class="add-button"
                      type="md-add"
                    />
                    <p slot="content" class="question-content">{{element.content}}</p>
                  </Panel>
                </Collapse>
              </transition-group>
            </draggable>
          </Scroll>
        </div>
        <!-- 右侧栏目 -->
        <div slot="right" class="demo-split-pane">
          <!-- 可拖动列表-组卷 -->
          <Scroll style="height:100%">
            <div style="display:flex;">
              <Button type="text" ghost style="margin-left:10px" @click="test">不要点我哦</Button>
              <h1 style="flex:1">试卷</h1>
              <Button type="info" style="margin-right:10px">加入分隔线</Button>
            </div>
            <draggable v-model="questionSelected" group="question">
              <transition-group>
                <Card v-for="element in questionSelected" :key="element.id" class="question-card">
                  <p slot="title" class="question-title">
                    {{element.name}}
                    <Icon
                      @click="remove(element.id)"
                      style="cursor:pointer"
                      class="remove-button"
                      type="md-close"
                    />
                  </p>
                  <p class="question-content">{{element.content}}</p>
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
import { constants } from "fs";
export default {
  name: "Test_Paper_Export_Mode",
  data() {
    return {
      questionSearched: [
        {
          id: 0,
          stem: "xswl",
          options:
            "我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容"
        },
        {
          id: 1,
          stem: "cxk",
          options:
            "我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容"
        },
        {
          id: 3,
          stem: "789",
          options:
            "我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容"
        },
        {
          id: 4,
          stem: "nmsl",
          options:
            "我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容"
        },
        {
          id: 5,
          stem: "多喝热水",
          options:
            "我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容"
        },
        {
          id: 6,
          stem: "少喝热水",
          options:
            "我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容"
        },
        {
          id: 7,
          stem: "不喝热水",
          options:
            "我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容"
        },
        {
          id: 8,
          stem: "不喝热水",
          options:
            "我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容"
        },
        {
          id: 9,
          stem: "不喝热水",
          options:
            "我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容"
        },
        {
          id: 10,
          stem: "不喝热水",
          options:
            "我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容"
        }
      ],
      questionSelected: [
        {
          id: 6,
          name: "测试样例呢",
          content:
            "我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容"
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
      ] ///已经有的学校
    };
  },
  mounted() {
    let that = this;
    //  获取知识点列表
    console.log("params:", this.$route.params);
    this.paperInfo = this.$route.params;
    this.paperInfo.ok = true;
    $.ajax({
      url: that.$site + "api/query_knowledgepoint",
      dataType: "json",
      data: {
        subject: "物理"
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
      .get(this.$site + "api/query_types")
      .then(res => {
        // console.log("query_types", res.data);
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
  },
  computed: {},
  methods: {
    test() {
      let that = this;
      console.log("恭喜你进入测试程序");
      this.$axios
        .post(that.$site + "api/search_question", {
          paperInfo: this.paperInfo,
          filters: this.questionFilters
        })
        .then(res => {
          console.log(res);
          var ok = res.data.ok;
          if (ok) {
            this.$Notice.success({
              title: "查找成功",
              desc: "不写点什么感觉过意不去呢"
            });
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
    flush_questions() {
      console.log("更新问题");
      this.$axios
        .post(this.$site + "api/search_question", {
          paperInfo: this.paperInfo,
          filters: this.questionFilters,
          knowledge_point: this.knowledgepoint_list,
          school_selected: this.school_selected
        })
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
    }
  },
  watch: {
    questionFilters() {
      console.log("questionFilters has changed", this.questionFilters);
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
}

.question-content {
  text-align: left;
}

.ivu-card-head {
  display: flex;
}

.add-button {
  float: right;

  font-size: 20px;
  margin-top: 8px;
}

.remove-button {
  line-height: 20px;
  float: right;
}

.ivu-collapse-item {
  text-align: left;
}

.ivu-collapse-header {
  font-size: 17px;
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
  margin: 0 5px;
}
.question-fliter {
  display: flex;
  align-items: center;
}
.ivu-layout {
  background: #fff;
}
</style>
