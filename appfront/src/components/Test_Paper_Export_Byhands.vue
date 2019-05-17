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
            <!-- 这里加个筛选器 -->
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
          <h1>试卷</h1>
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
export default {
  name: "Test_Paper_Export_Mode",
  data() {
    return {
      questionSearched: [
        {
          id: 0,
          name: "xswl",
          content:
            "我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容"
        },
        {
          id: 1,
          name: "cxk",
          content:
            "我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容"
        },
        {
          id: 3,
          name: "789",
          content:
            "我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容"
        },
        {
          id: 4,
          name: "nmsl",
          content:
            "我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容"
        },
        {
          id: 5,
          name: "多喝热水",
          content:
            "我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容"
        },
        {
          id: 6,
          name: "少喝热水",
          content:
            "我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容"
        },
        {
          id: 7,
          name: "不喝热水",
          content:
            "我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容"
        },
        {
          id: 8,
          name: "不喝热水",
          content:
            "我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容"
        },
        {
          id: 9,
          name: "不喝热水",
          content:
            "我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容我是题目的内容"
        },
        {
          id: 10,
          name: "不喝热水",
          content:
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
      formItem: {}
    };
  },
  mounted() {},
  computed: {},
  methods: {
    add(id) {
      this.questionSearched.forEach((item, index, arr) => {
        if (item.id == id) {
          this.questionSelected.push(item);
          arr.splice(index, 1);
        }
      });
    },
    remove(id) {
      this.questionSelected.forEach((item, index, arr) => {
        if (item.id == id) {
          this.questionSearched.push(item);
          arr.splice(index, 1);
        }
      });
    }
  },
  components: {
    draggable
  }
};
</script>

<style>
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

body {
  height: 100%;
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
</style>
