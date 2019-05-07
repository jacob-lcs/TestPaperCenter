<template>
  <div>

    <!--  添加试题dialog  -->
    <Modal v-model="modal12" draggable scrollable title="创建试题" width="90vw">

      <p slot="header" style="text-align:center">
        <Icon type="ios-download-outline"></Icon>
        <span>添加试题</span>
      </p>
      <div>

        <div style="margin-top: 15px; margin-bottom:15px; text-align: center">
          <!--    试卷名称输入    -->
          <Input size="large" v-model="paper_name" placeholder="请输入试卷名称" style="width: 300px;"/>
          <!--    学校名称输入    -->
          <Input size="large" v-model="school_name" placeholder="请输入学校名称" style="width: 300px;"/>
        </div>
        <!--  年级选择器  -->
        <Select v-model="grade" style="width:200px" transfer placeholder="请选择年级">
          <Option v-for="item in grade_list" :value="item.value" :key="item.value">{{ item.label }}</Option>
        </Select>
        <!--  科目选择器  -->
        <Select v-model="paper_subject" style="width:200px" transfer placeholder="请选择科目">
          <Option v-for="item in subject_list" :value="item.value" :key="item.value">{{ item.label }}</Option>
        </Select>
        <!--  题型选择器  -->
        <Select v-model="topic" style="width:200px" @on-change="topic_change" transfer placeholder="请选择题目类型">
          <Option v-for="item in topicList" :value="item.value" :key="item.value">{{ item.label }}</Option>
        </Select>
        <!--  试题难度选择器  -->
        <Select v-model="question_difficulty" style="width:200px" transfer placeholder="请选择试题难度">
          <Option v-for="item in question_difficulty_list" :value="item.value" :key="item.value">{{ item.label }}
          </Option>
        </Select>
        <!--    试卷年份选择器    -->
        <DatePicker type="year" @on-change="select_year_change" format="yyyy" placeholder="请选择试卷年份" style="width: 200px"
                    transfer></DatePicker>
        <br>

        <!--  单选题  -->
        <div v-if="topic === '单选题'">

          <!--     输入题干     -->
          <mavon-editor v-model="question_content" ref=md @imgAdd="$imgAdd" @imgDel="$imgDel"
                        placeholder="请输入题干...." style="margin-top: 15px"></mavon-editor>
          <Divider>选项</Divider>

          <!-- 选择题选项 -->
          <RadioGroup v-model="question_answer_chosen" vertical>
            <div v-for="select_option in select_options">
              <Radio style="margin-top: 15px" size="large" :label="select_option.label"></Radio>
              <mavon-editor v-model="select_option.content" ref=md @imgAdd="$imgAdd" @imgDel="$imgDel"
                            placeholder="请输入选项内容...." style="margin-top: 5px;"></mavon-editor>
            </div>
          </RadioGroup>
          <!--  知识点标签  -->
          <div>
            <Tag v-for="item in knowledgepoint_list" :key="item" :name="item" closable @on-close="knowledgepoint_close"
                 style="margin-top: 15px">
              {{ item }}
            </Tag>
            <Cascader :data="knowledge" @on-change="knowledge_point_change"
                      transfer style="margin-top: 15px; width: 200px" change-on-select
                      placeholder="请选择知识点标签"></Cascader>
          </div>

          <!--     添加和删除选项     -->
          <div style="margin-top: 15px">
            <Button shape="circle" icon="md-add" type="primary" @click="add_select_option">添加选项</Button>
            <Button shape="circle" icon="md-close" type="error" @click="delete_select_option">删除选项</Button>
          </div>
        </div>

        <!--  多选题  -->
        <div v-if="topic === '多选题'">

          <!--     输入题干     -->
          <mavon-editor v-model="question_content" ref=md @imgAdd="$imgAdd" @imgDel="$imgDel"
                        placeholder="请输入题干...." style="margin-top: 15px"></mavon-editor>
          <Divider>选项</Divider>

          <!--     选择题选项    -->
          <CheckboxGroup v-model="multiple_question_chosen" vertical>
            <div v-for="select_option in select_options">
              <Checkbox style="margin-top: 15px" size="large" :label="select_option.label"></Checkbox>
              <mavon-editor v-model="select_option.content" ref=md @imgAdd="$imgAdd" @imgDel="$imgDel"
                            placeholder="请输入选项内容...." style="margin-top: 5px;"></mavon-editor>
            </div>
          </CheckboxGroup>
          <!--     知识点标签     -->
          <div>
            <Tag v-for="item in knowledgepoint_list" :key="item" :name="item" closable @on-close="knowledgepoint_close"
                 style="margin-top: 15px">
              {{ item }}
            </Tag>
            <Cascader :data="knowledge" @on-change="knowledge_point_change"
                      transfer style="margin-top: 15px; width: 200px" change-on-select
                      placeholder="请选择知识点标签"></Cascader>
          </div>

          <!--     添加和删除选项     -->
          <div style="margin-top: 15px">
            <Button shape="circle" icon="md-add" type="primary" @click="add_select_option">添加选项</Button>
            <Button shape="circle" icon="md-close" type="error" @click="delete_select_option">删除选项</Button>
          </div>
        </div>

        <!--   简答题与计算题     -->
        <div v-if="topic === '简答题' || topic === '计算题'">

          <!--     输入题干     -->
          <mavon-editor v-model="question_content" ref=md @imgAdd="$imgAdd" @imgDel="$imgDel"
                        placeholder="请输入题干...." style="margin-top: 15px"></mavon-editor>
          <Divider>答案</Divider>

          <!--     问答题答案    -->
          <mavon-editor v-model="question_answer" ref=md @imgAdd="$imgAdd" @imgDel="$imgDel"
                        placeholder="请输入答案...." style="margin-top: 5px;"></mavon-editor>
          <!--     知识点标签     -->
          <div>
            <Tag v-for="item in knowledgepoint_list" :key="item" :name="item" closable @on-close="knowledgepoint_close"
                 style="margin-top: 15px">
              {{ item }}
            </Tag>
            <Cascader :data="knowledge" @on-change="knowledge_point_change"
                      transfer style="margin-top: 15px; width: 200px" change-on-select
                      placeholder="请选择知识点标签"></Cascader>
          </div>

        </div>

        <!--   填空题     -->
        <div v-if="topic === '填空题'">

          <!--     输入题干     -->
          <mavon-editor v-model="question_content" ref=md @imgAdd="$imgAdd" @imgDel="$imgDel"
                        placeholder="请输入题干，空使用”____“表示" style="margin-top: 15px"></mavon-editor>
          <Divider>答案</Divider>

          <!--     填空题答案    -->
          <mavon-editor v-model="question_answer" ref=md @imgAdd="$imgAdd" @imgDel="$imgDel"
                        placeholder="请输入填空题答案，答案与答案之间使用”；；“分离" style="margin-top: 5px;"></mavon-editor>
          <!--     知识点标签     -->
          <div>
            <Tag v-for="item in knowledgepoint_list" :key="item" :name="item" closable @on-close="knowledgepoint_close"
                 style="margin-top: 15px">
              {{ item }}
            </Tag>
            <Cascader :data="knowledge" @on-change="knowledge_point_change"
                      transfer style="margin-top: 15px; width: 200px" change-on-select
                      placeholder="请选择知识点标签"></Cascader>
          </div>

        </div>

        <!--    判断题    -->
        <div v-if="topic === '判断题'">

          <!--     输入题干     -->
          <mavon-editor v-model="question_content" ref=md @imgAdd="$imgAdd" @imgDel="$imgDel"
                        placeholder="请输入题干...." style="margin-top: 15px"></mavon-editor>
          <Divider>答案</Divider>

          <!--  判断题答案  -->
          <div>
            <i-switch size="large" v-model="true_or_false" true-value="1" false-value="0">
              <span slot="open">正确</span>
              <span slot="close">错误</span>
            </i-switch>
          </div>
          <!--     知识点标签     -->
          <div>
            <Tag v-for="item in knowledgepoint_list" :key="item" :name="item" closable @on-close="knowledgepoint_close"
                 style="margin-top: 15px">
              {{ item }}
            </Tag>
            <Cascader :data="knowledge" @on-change="knowledge_point_change"
                      transfer style="margin-top: 15px; width: 200px" change-on-select
                      placeholder="请选择知识点标签"></Cascader>
          </div>

        </div>


      </div>
      <div slot="footer" style="text-align: center;">
        <Button type="primary" icon="md-document" @click="save_and_close">保存并关闭</Button>
        <Button icon="md-flash" @click="save_and_dont_close">保存并新增</Button>
        <Button type="error" icon="ios-close" @click="close_import_paper">关闭</Button>
      </div>
    </Modal>


    <div class="single-choice">
      <Row style="background:#eee;padding:20px">
        <Col span="25">
          <Card :bordered="false">
            <Row>
              <Col span="12" style="text-align: left; font-size: 20px">
                <p>题目列表</p>
              </Col>
              <Col span="12" style="text-align: right; ">
                <Button icon="md-add" type="primary" style="font-size: 15px;"
                        @click="modal12 = true">添加试题
                </Button>
              </Col>
            </Row>
          </Card>
        </Col>
      </Row>
      <!--   题目表格   -->
      <Table border :columns="columns1" :data="data1"></Table>


    </div>
  </div>
</template>

<script>
  import {mavonEditor} from 'mavon-editor'

  export default {
    name: "Test_Paper_Import",
    data() {
      return {
        paper_name: '',  // 试卷名称
        paper_year: '',  // 试卷年份
        paper_subject: '', // 已经选择的试卷科目
        subject_list: [],  // 科目选择器的科目列表
        modal12: false,  // 导入试题对话框显示标志位
        topicList: [],  // 可供选择的题型
        topic: '',  //目前选择的题型
        question_content: '',  // 题干
        columns1: [    // 列名
          {
            title: '题干',
            key: 'question_content',
            render: (h, params) => {
              return h('div', [
                h('Icon', {
                  props: {
                    type: 'person'
                  }
                }),
                h('strong', params.row.name)
              ]);
            }
          },
          {
            title: '答案',
            key: 'question_answer'
          },
          {
            title: '题目类型',
            key: 'question_type'
          },
          {
            title: '题目难度',
            key: 'question_difficulty'
          },
          {
            title: '试卷名称',
            key: 'paper_name'
          },
          {
            title: 'Action',
            key: 'action',
            width: 150,
            align: 'center',
            render: (h, params) => {
              return h('div', [
                h('Button', {
                  props: {
                    type: 'primary',
                    size: 'small'
                  },
                  style: {
                    marginRight: '5px'
                  },
                  on: {
                    click: () => {
                      console.log(params.index)
                    }
                  }
                }, 'View'),
                h('Button', {
                  props: {
                    type: 'error',
                    size: 'small'
                  },
                  on: {
                    click: () => {
                      this.$Modal.confirm({
                        title: 'Title',
                        content: '<p>确定删除此题吗</p>',
                        onOk: () => {
                          this.$Message.info('Clicked ok');
                        },
                        onCancel: () => {
                          this.$Message.info('Clicked cancel');
                        }
                      });
                    }
                  }
                }, 'Delete')
              ]);
            }
          }
        ],
        data1: [],// 题目数据
        select_options: [],  // 选择题选项
        question_difficulty: '',  // 题目难度
        question_difficulty_list: [],  // 题目难度列表
        knowledgepoint_list: [],  // 题目知识点列表
        knowledge: [],  // 级联选择器的知识点列表
        grade_list: [],  // 年级列表
        grade: '',  // 已经选择的年级
        question_answer_chosen: '',  // 选择的正确答案
        question_answer: '',  // 生成的正确答案
        option_title: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'],  // 选项标号
        school_name: '',  // 输入的学校名称
        import_success: false,  // 导入是否成功标志位
        multiple_question_chosen: [],  // 多选题选择的答案
        true_or_false: '0',  // 判断题答案

      }
    },
    methods: {

      // 添加选项
      add_select_option() {
        if (this.select_options.length === 24) {
          this.$Message.warning('最多只能添加24个选项哦');
        } else {
          let label = this.option_title[this.select_options.length];
          let con = {
            content: '',
            label: label
          };
          this.select_options.push(con)
        }
      },

      // 删除选项
      delete_select_option() {
        this.select_options.pop()
      },


      // 题型发生变化
      topic_change() {
        console.log(this.topic)
      },

      // 图片上传
      $imgAdd(pos, $file) {
        let file = Bmob.File($file.name, $file);
        file.save().then(res => {
          console.log(res.length);
          console.log(res);
          // 将图片链接改为图片地址
          this.$refs.md.$img2Url(pos, res[0]['url']);
        })
      },

      // 删除图片触发的操作
      $imgDel(pos, $file) {

      },
      // 关闭知识点标签触发的事件
      knowledgepoint_close(event, name) {
        const index = this.knowledgepoint_list.indexOf(name);
        this.knowledgepoint_list.splice(index, 1);
      },

      // 知识点级联选择变化触发的事件
      knowledge_point_change(value, selectedData) {
        console.log("触发级联选择器change事件");
        if (this.knowledgepoint_list.indexOf(value[value.length - 1]) === -1) {
          this.knowledgepoint_list.push(value[value.length - 1]);
        }
      },

      // 关闭导入试题对话框触发的事件
      close_import_paper() {
        this.modal12 = false
      },

      // 生成单选题答案
      generate_signal_selection_answer() {
        let that = this;
        for (var i = 0; i < that.select_options.length; i++) {
          if (that.question_answer_chosen === that.select_options[i]['label']) {
            that.question_answer = that.question_answer.concat("lcshchzlm" + that.select_options[i]['label'] + ".%$@#$%" + that.select_options[i]['content'])
          } else {
            that.question_answer = that.question_answer.concat("lcshchzlm" + that.select_options[i]['label'] + "." + that.select_options[i]['content'])
          }
        }
        console.log("生成的答案为：", that.question_answer)
      },


      // 生成多选题答案
      generate_multiple_selection_answer() {
        let that = this;
        that.question_answer = '';
        for (var i = 0; i < that.select_options.length; i++) {
          if (that.multiple_question_chosen.indexOf(that.select_options[i]['label']) !== -1) {
            that.question_answer = that.question_answer.concat("lcshchzlm" + that.select_options[i]['label'] + ".%$@#$%" + that.select_options[i]['content'])
          } else {
            that.question_answer = that.question_answer.concat("lcshchzlm" + that.select_options[i]['label'] + "." + that.select_options[i]['content'])
          }
        }
        console.log("生成的答案为：", that.question_answer)
      },

      // 导入试题
      import_question() {
        console.log("import_question()");
        let that = this;
        let kk = {'list': that.knowledgepoint_list};
        $.ajax({
          url: that.$site + "api/save_single_topic_selection",
          dataType: "json",
          data: {
            school_name: that.school_name,
            paper_name: that.paper_name,
            paper_year: that.paper_year,
            grade: that.grade,
            subject: that.paper_subject,
            question_type: that.topic,
            question_stem: that.question_content,
            question_answer: that.question_answer,
            question_difficult: that.question_difficulty,
            question_knowledgepoints: kk
          },
          success: function (data) {
            console.log(data);
            if (data['res'] === "success") {
              that.$Message.info("导入成功！");
              that.successfully_import_clear();
            } else {
              that.$Message.warning("请检查网络！")
            }
          }
        });
      },


      // 检查试卷基本信息有无没有输入的数据
      check_paper_content() {
        let that = this;
        if (that.knowledgepoint_list.length === 0) {
          that.$Message.warning("请选择知识点");
          return false;
        } else if (that.paper_year === '') {
          that.$Message.warning("请输入年份");
          return false;
        } else if (that.paper_name === '') {
          that.$Message.warning("请输入试卷名称");
          return false;
        } else if (that.paper_subject === '') {
          that.$Message.warning("请选择试卷科目");
          return false;
        } else if (that.topic === '') {
          that.$Message.warning("请选择题目类型");
          return false;
        } else if (that.grade === '') {
          that.$Message.warning("请输入年级");
          return false;
        } else if (that.school_name === '') {
          that.$Message.warning("请输入学校名称");
          return false;
        } else if (that.question_difficulty === '') {
          that.$Message.warning("请选择题目难度");
          return false;
        } else {
          return true;
        }
      },


      // 检查单选题输入的内容
      check_signal_select_content() {
        let that = this;
        if (that.question_content === '') {
          that.$Message.warning("请输入题目内容");
          return false;
        } else if (that.question_answer_chosen === '') {
          that.$Message.warning("请选择正确答案");
          return false;
        } else if (!that.check_select_options_has_null()) {
          that.$Message.warning("请输入选项内容");
          return false;
        } else {
          return true;
        }
      },

      // 检查多选题输入的内容
      check_multiple_select_content() {
        let that = this;
        if (that.multiple_choice_content === '') {
          that.$Message.warning("请输入题目内容");
          return false;
        } else if (that.multiple_question_chosen.length === 0) {
          that.$Message.warning("请选择正确答案");
          return false;
        } else if (!that.check_select_options_has_null()) {
          that.$Message.warning("请输入选项内容");
          return false;
        } else {
          return true;
        }
      },


      // 检查问答题输入的内容
      check_essay_question_content() {
        let that = this;
        if (that.question_content === '') {
          that.$Message.warning("请输入题目内容");
          return false;
        } else if (that.question_answer === '') {
          that.$Message.warning("请输入正确答案");
          return false;
        } else {
          return true;
        }
      },


      // 判断选择题选项是否有空
      check_select_options_has_null() {
        let that = this;
        for (var i = 0; i < that.select_options.length; i++) {
          if (that.select_options[i]['content'] === '') {
            return false;
          }
        }
        return true;
      },

      // 保存并关闭对话框
      save_and_close() {
        console.log("导入试题中......");
        let that = this;
        if (that.check_paper_content()) {
          console.log("进入第二级");
          if (that.topic === "单选题") {
            if (that.check_signal_select_content()) {
              that.generate_signal_selection_answer();
              that.import_question();
              that.modal12 = false;
            }
          } else if (that.topic === "多选题") {
            if (that.check_multiple_select_content()) {
              that.generate_multiple_selection_answer();
              that.import_question();
              that.modal12 = false;
            }
          } else if (that.topic === "简答题" || that.topic === "计算题" || that.topic === "判断题") {
            if (that.check_essay_question_content()) {
              that.import_question();
              that.modal12 = false;
            }
          } else if (that.topic === "判断题") {
            if(that.question_content === ''){
              that.$Message.warning("请先输入题干");
            }else{
              if (that.true_or_false === '1'){
                that.question_answer = "正确";
                that.import_question();
                that.modal12 = false;
              } else {
                that.question_answer = "错误";
                that.import_question();
                that.modal12 = false;
              }
            }
          }
        }
      },


      // 导入试题成功则清空数据
      successfully_import_clear() {
        let that = this;
        console.log("清空数据....");
        that.question_answer_chosen = '';
        that.question_content = '';
        that.select_options = [];
        that.knowledgepoint_list = [];
        that.question_answer_chosen = '';
        that.question_answer = '';
        that.multiple_question_chosen = [];
        that.multiple_choice_content = '';
      },


      // 保存并导入下一个题目
      save_and_dont_close() {
        let that = this;
        console.log(that.multiple_question_chosen);
        console.log(that.true_or_false);
        if (that.check_paper_content()) {
          console.log("进入第二级");
          if (that.topic === "单选题") {
            if (that.check_signal_select_content()) {
              that.generate_signal_selection_answer();
              that.import_question();
            }
          } else if (that.topic === "多选题") {
            if (that.check_multiple_select_content()) {
              that.generate_multiple_selection_answer();
              that.import_question();
            }
          } else if (that.topic === "简答题" || that.topic === "计算题" || that.topic === "判断题") {
            if (that.check_essay_question_content()) {
              that.import_question();
            }
          } else if (that.topic === "判断题") {
            if(that.question_content === ''){
              that.$Message.warning("请先输入题干");
            }else{
              if (that.true_or_false === '1'){
                that.question_answer = "正确";
                that.import_question();
              } else {
                that.question_answer = "错误";
                that.import_question();
              }
            }
          }
        }

      },


      // 日期选择器改变
      select_year_change(year) {
        this.paper_year = year;
        console.log(this.paper_year)
      }
    },

    mounted() {
      let that = this;
      // 路径保护
      if (sessionStorage.getItem('per_name') == null) {
        this.$router.push("/")
      } else {
        console.log(sessionStorage.getItem('per_name'))
      }

      //  获取题目难度列表
      $.ajax({
        url: that.$site + "api/query_difficulty",
        dataType: "json",
        data: {},
        success: function (data) {
          console.log(data);
          for (var i = 0; i < data.length; i++) {
            that.question_difficulty_list.push({
              value: data[i]['name'],
              label: data[i]['name']
            })
          }
        }
      });

      //  获取题目类型列表
      $.ajax({
        url: that.$site + "api/query_types",
        dataType: "json",
        data: {},
        success: function (data) {
          console.log(data);
          for (var i = 0; i < data.length; i++) {
            that.topicList.push({
              value: data[i]['name'],
              label: data[i]['name']
            })
          }
        }
      })

      //  获取知识点列表
      $.ajax({
        url: that.$site + "api/query_knowledgepoint",
        dataType: "json",
        data: {},
        success: function (data) {
          console.log(data);
          for (var i = 0; i < data.length; i++) {
            that.knowledge.push(data[i])
          }
        }
      });

      //  获取科目列表
      $.ajax({
        url: that.$site + "api/query_subjects",
        dataType: "json",
        data: {},
        success: function (data) {
          console.log(data);
          for (var i = 0; i < data.length; i++) {
            that.subject_list.push({
              value: data[i]['name'],
              label: data[i]['name']
            })
          }
        }
      });


      //  获取年级列表
      $.ajax({
        url: that.$site + "api/query_grades",
        dataType: "json",
        data: {},
        success: function (data) {
          console.log(data);
          for (var i = 0; i < data.length; i++) {
            that.grade_list.push({
              value: data[i]['name'],
              label: data[i]['name']
            })
          }
        }
      })
    }
  }
</script>

<style scoped>
  .single-choice {
    margin-left: 200px;
    margin-right: 200px;
    margin-top: 30px;
  }
</style>
