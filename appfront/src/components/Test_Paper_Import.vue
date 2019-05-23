<template>
  <div>
    <!--  添加试题dialog  -->
    <Modal v-model="modal12" scrollable title="创建试题" width="90vw">

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
        <Select v-model="paper_subject" style="width:200px" transfer placeholder="请选择科目" @on-change="subject_change">
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


        <!--  选择题  -->
        <div v-if="topic === '选择题'">

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
          <div v-if="paper_subject !== ''">
            <Tag v-for="item in knowledgepoint_list" :key="item" :name="item" closable @on-close="knowledgepoint_close"
                 style="margin-top: 15px">
              {{ item }}
            </Tag>
            <Row>
              <div class="inline" style="margin-top: 15px; display: flex">
                <Cascader :data="knowledge" @on-change="knowledge_point_change"
                          transfer style=" width: 200px" change-on-select
                          placeholder="请选择知识点标签"></Cascader>
                <Poptip trigger="hover" content="没有找到知识点？点击添加">
                  <Icon type="md-add" size="20" style="margin-top: 5px; margin-left: 10px;cursor: pointer"
                        @click="add_knowledge_point"/>
                </Poptip>
              </div>
            </Row>
          </div>

          <!--     添加和删除选项     -->
          <div style="margin-top: 15px">
            <Button shape="circle" icon="md-add" type="primary" @click="add_select_option">添加选项</Button>
            <Button shape="circle" icon="md-close" type="error" @click="delete_select_option">删除选项</Button>
          </div>
        </div>

        <!--   简答题与计算题     -->
        <div v-if="topic === '简答题'||topic === '应用题'||topic === '作图题' ||topic === '改写句子'||topic === '作文' ||topic === '听力'||topic === '实验题'||topic === '完形填空'||topic === '将单词改为适当形式填空' ||topic === '现代文阅读' ||topic === '文言文阅读' || topic === '解答题' || topic === '计算题' || topic === '阅读理解' || topic === '语言表达' || topic === '诗歌鉴赏'">

          <!--     输入题干     -->
          <mavon-editor v-model="question_content" ref=md @imgAdd="$imgAdd" @imgDel="$imgDel"
                        placeholder="请输入题干...." style="margin-top: 15px"></mavon-editor>
          <Divider>答案</Divider>

          <!--     问答题答案    -->
          <mavon-editor v-model="question_answer" ref=md @imgAdd="$imgAdd" @imgDel="$imgDel"
                        placeholder="请输入答案...." style="margin-top: 5px;"></mavon-editor>
          <!--     知识点标签     -->
          <div v-if="paper_subject !== ''">
            <Tag v-for="item in knowledgepoint_list" :key="item" :name="item" closable @on-close="knowledgepoint_close"
                 style="margin-top: 15px">
              {{ item }}
            </Tag>
            <Row>
              <div class="inline" style="margin-top: 15px; display: flex">
                <Cascader :data="knowledge" @on-change="knowledge_point_change"
                          transfer style=" width: 200px" change-on-select
                          placeholder="请选择知识点标签"></Cascader>
                <Poptip trigger="hover" content="没有找到知识点？点击添加">
                  <Icon type="md-add" size="20" style="margin-top: 5px; margin-left: 10px;cursor: pointer"
                        @click="add_knowledge_point"/>
                </Poptip>
              </div>
            </Row>
          </div>

        </div>

        <!--   填空题     -->
        <div v-if="topic === '填空题'||topic === '默写'||topic === '选词填空'">

          <!--     输入题干     -->
          <mavon-editor v-model="question_content" ref=md @imgAdd="$imgAdd" @imgDel="$imgDel"
                        placeholder="请输入题干，空使用”____“表示" style="margin-top: 15px"></mavon-editor>
          <Divider>答案</Divider>

          <!--     填空题答案    -->
          <mavon-editor v-model="question_answer" ref=md @imgAdd="$imgAdd" @imgDel="$imgDel"
                        placeholder="请输入答案，答案与答案之间使用”；；“分离" style="margin-top: 5px;"></mavon-editor>
          <!--     知识点标签     -->
          <div v-if="paper_subject !== ''">
            <Tag v-for="item in knowledgepoint_list" :key="item" :name="item" closable @on-close="knowledgepoint_close"
                 style="margin-top: 15px">
              {{ item }}
            </Tag>
            <Row>
              <div class="inline" style="margin-top: 15px; display: flex">
                <Cascader :data="knowledge" @on-change="knowledge_point_change"
                          transfer style=" width: 200px" change-on-select
                          placeholder="请选择知识点标签"></Cascader>
                <Poptip trigger="hover" content="没有找到知识点？点击添加">
                  <Icon type="md-add" size="20" style="margin-top: 5px; margin-left: 10px;cursor: pointer"
                        @click="add_knowledge_point"/>
                </Poptip>
              </div>
            </Row>
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
          <div v-if="paper_subject !== ''">
            <Tag v-for="item in knowledgepoint_list" :key="item" :name="item" closable @on-close="knowledgepoint_close"
                 style="margin-top: 15px">
              {{ item }}
            </Tag>
            <Row>
              <div class="inline" style="margin-top: 15px; display: flex">
                <Cascader :data="knowledge" @on-change="knowledge_point_change"
                          transfer style=" width: 200px" change-on-select
                          placeholder="请选择知识点标签"></Cascader>
                <Poptip trigger="hover" content="没有找到知识点？点击添加">
                  <Icon type="md-add" size="20" style="margin-top: 5px; margin-left: 10px;cursor: pointer"
                        @click="add_knowledge_point"/>
                </Poptip>
              </div>
            </Row>
          </div>

        </div>


      </div>
      <div slot="footer" style="text-align: center;">
        <Button type="primary" icon="md-document" @click="save_and_close">保存并关闭</Button>
        <Button icon="md-flash" @click="save_and_dont_close">保存并新增</Button>
        <Button type="error" icon="ios-close" @click="close_import_paper">关闭</Button>
      </div>
    </Modal>
    <!--  添加知识点对话框  -->
    <Modal v-model="add_knowledge_point_show" mask scrollable title="添加知识点" :z-index="z_index" :mask-closable="false"
           @on-ok="add_knowledge_point_commit">
      <div>
        请输入知识点：&emsp;&emsp;
        <Input placeholder="请输入知识点" style="width: auto" v-model="add_knowledge_point_input"/>
      </div>
      <div style="margin-top: 25px">
        请选择上级知识点:&emsp;
        <Select v-model="select_add_knowledge" style="width:200px" placeholder="请选择上级知识点">
          <Option v-for="item in knowledgepoint_list_add" :value="item.value" :key="item.value">{{ item.label }}
          </Option>
        </Select>
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
              <Col span="4" style="text-align: right; ">
                <Button icon="ios-cloud-download" type="primary" style="font-size: 15px;" @click="download_template">
                  下载模板
                </Button>
              </Col>
              <Col span="4" style="text-align: right; ">
                <Upload action="//127.0.0.1:8000/api/upload_excel" :on-success="upload_success">
                  <Button type="primary" style="height: 38px; font-size: 15px;" icon="ios-cloud-upload">上传文件</Button>
                </Upload>
              </Col>
              <Col span="4" style="text-align: right; ">
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
      <Page :total="data_count" :current="current_page" @on-change="page_change" :page-size="page_count"
            style="margin-bottom: 20px; margin-top: 20px"/>
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
          },
          {
            title: '答案',
            key: 'question_answer'
          },
          {
            title: '题目选项',
            key: 'question_options'
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
                      console.log(params)
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
                          this.delete_question(params.row.question_content, params.row.question_answer, params.row.question_type, params.row.question_difficulty, params.row.paper_name);
                        },
                        onCancel: () => {

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
        add_knowledge_point_show: false,  // 添加知识点对话框是否显示
        select_add_knowledge: '',  // 选择添加的知识点
        knowledgepoint_list_add: [],  // 选择添加知识点显示的知识点列表
        add_knowledge_point_input: '',  // 添加的知识点
        z_index: 1002,  // modal z-index值
        data_count: 0,  // 数据总数
        page_count: 30,  // 一页显示的数据数量
        current_page: 1, // 当前页码
        true_answer:'',

      }
    },
    methods: {

      // 添加选项
      add_select_option() {
        if (this.select_options.length === 24) {
          this.$Notice.warning({
            title: '最多只能添加24个选项哦'
          })
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
          that.question_answer = that.question_answer.concat(that.select_options[i]['label'] + "." + that.select_options[i]['content'] + "\n")
        }
        console.log("生成的答案为：", that.question_answer)
      },


      // 生成多选题答案
      generate_multiple_selection_answer() {
        let that = this;
        console.log("选择题答案为：", that.multiple_question_chosen.length);
        that.question_answer = '';
        for(var j=0; j<that.multiple_question_chosen.length; j++){
          if (j === 0){
            that.true_answer = '';
          }
          that.true_answer +=(that.multiple_question_chosen[j] + '；');
        }
        for (var i = 0; i < that.select_options.length; i++) {
          console.log("进入2循环");
          that.question_answer = that.question_answer.concat(that.select_options[i]['label'] + "." + that.select_options[i]['content'] + "\n")
        }
        console.log("生成的答案为：",that.true_answer);

      },

      // 导入试题start
      import_question() {
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
            question_answer: that.true_answer,
            question_options: that.question_answer,
            question_difficult: that.question_difficulty,
            question_knowledgepoints: kk
          },
          success: function (data) {
            console.log(data);
            if (data['res'] === "success") {
              that.$Notice.success({
                title: '导入成功'
              });

              that.successfully_import_clear();
            } else {
              that.$Notice.warning({
                title: '请检查网络'
              });
            }
          }
        });
      },


      // 检查试卷基本信息有无没有输入的数据
      check_paper_content() {
        let that = this;
        if (that.knowledgepoint_list.length === 0) {
          that.$Notice.warning({
            title: '请选择知识点'
          });
          return false;
        } else if (that.paper_year === '') {
          that.$Notice.warning({
            title: '请输入年份'
          });
          return false;
        } else if (that.paper_name === '') {
          that.$Notice.warning({
            title: '请输入试卷名称'
          });
          return false;
        } else if (that.paper_subject === '') {
          that.$Notice.warning({
            title: '请选择试卷科目'
          });
          return false;
        } else if (that.topic === '') {
          that.$Notice.warning({
            title: '请选择题目类型'
          });
          return false;
        } else if (that.grade === '') {
          that.$Notice.warning({
            title: '请输入年级'
          });
          return false;
        } else if (that.school_name === '') {
          that.$Notice.warning({
            title: '请输入学校名称'
          });
          return false;
        } else if (that.question_difficulty === '') {
          that.$Notice.warning({
            title: '请选择题目难度'
          });
          return false;
        } else {
          return true;
        }
      },


      // 检查单选题输入的内容
      check_signal_select_content() {
        let that = this;
        if (that.question_content === '') {
          that.$Notice.warning({
            title: '请输入题目内容'
          });
          return false;
        }  else if (!that.check_select_options_has_null()) {
          that.$Notice.warning({
            title: '请输入选项内容'
          });
          return false;
        } else {
          return true;
        }
      },

      // 检查多选题输入的内容
      check_multiple_select_content() {
        let that = this;
        if (that.multiple_choice_content === '') {
          that.$Notice.warning({
            title: '请输入题目内容'
          });
          return false;
        }else if (!that.check_select_options_has_null()) {
          that.$Notice.warning({
            title: '请输入选项内容'
          });
          return false;
        } else {
          return true;
        }
      },


      // 检查问答题输入的内容
      check_essay_question_content() {
        let that = this;
        if (that.question_content === '') {
          that.$Notice.warning({
            title: '请输入题目内容'
          });
          return false;
        } else if (that.question_answer === '') {
          that.$Notice.warning({
            title: '请选择正确答案'
          });
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
        let that = this;
        if (that.check_paper_content()) {
          if (that.topic === "选择题") {
            if (that.check_multiple_select_content()) {
              that.generate_multiple_selection_answer();
              that.import_question();
              that.modal12 = false;
            }
          } else if (that.topic === '填空题'||that.topic === '应用题'||that.topic === '默写'||that.topic === '选词填空'||that.topic === '简答题'||that.topic === '作图题' ||that.topic === '改写句子'||that.topic === '作文' ||that.topic === '听力'||that.topic === '实验题'||that.topic === '完形填空'||that.topic === '将单词改为适当形式填空' ||that.topic === '现代文阅读' ||that.topic === '文言文阅读' || that.topic === '解答题' || that.topic === '计算题' || that.topic === '阅读理解' || that.topic === '语言表达' || that.topic === '诗歌鉴赏') {
            if (that.check_essay_question_content()) {
              that.import_question();
              that.modal12 = false;
            }
          } else if (that.topic === "判断题") {
            if (that.question_content === '') {
              that.$Notice.warning({
                title: '情输入题干'
              });
            } else {
              if (that.true_or_false === '1') {
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
        if (that.check_paper_content()) {
          console.log("进入第二级");
          if (that.topic === "选择题") {
            if (that.check_multiple_select_content()) {
              that.generate_multiple_selection_answer();
              that.import_question();
            }
          } else if (that.topic === '填空题'||that.topic === '应用题'||that.topic === '默写'||that.topic === '选词填空'||that.topic === '简答题'||that.topic === '作图题' ||that.topic === '改写句子'||that.topic === '作文' ||that.topic === '听力'||that.topic === '实验题'||that.topic === '完形填空'||that.topic === '将单词改为适当形式填空' ||that.topic === '现代文阅读' ||that.topic === '文言文阅读' || that.topic === '解答题' || that.topic === '计算题' || that.topic === '阅读理解' || that.topic === '语言表达' || that.topic === '诗歌鉴赏') {
            if (that.check_essay_question_content()) {
              that.import_question();
            }
          } else if (that.topic === "判断题") {
            if (that.question_content === '') {
              that.$Notice.warning({
                title: '请输入题干'
              });
            } else {
              if (that.true_or_false === '1') {
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
      },

      // 科目选择器的值发生改变
      subject_change() {
        let that = this;
        //  获取知识点列表
        that.topic = '';
        $.ajax({
          url: that.$site + "api/query_knowledgepoint",
          dataType: "json",
          data: {
            subject: that.paper_subject
          },
          success: function (data) {
            console.log(data);
            that.knowledge = [];
            for (var i = 0; i < data.length; i++) {
              that.knowledge.push(data[i])
            }
          }
        });

        //  获取添加知识点时需要的知识点列表
        $.ajax({
          url: that.$site + "api/query_knowledge_point_list",
          dataType: "json",
          data: {
            subject: that.paper_subject
          },
          success: function (data) {
            console.log(data);
            that.knowledgepoint_list_add = [];
            console.log("此时that.knowledgepoint_list_add的长度为", that.knowledgepoint_list_add.length);
            for (var i = 0; i < data.length; i++) {
              that.knowledgepoint_list_add.push({
                value: data[i]['name'],
                label: data[i]['name']
              })
            }
          }
        });
        that.query_question_types(that.paper_subject)
      },

      // 添加知识点
      add_knowledge_point() {
        console.log("触发事件");
        this.add_knowledge_point_show = true
      },

      // 确定添加知识点触发的事件
      add_knowledge_point_commit() {
        let that = this;
        $.ajax({
          url: that.$site + "api/add_knowledge_points",
          dataType: "json",
          data: {
            child_knowledge_point: that.add_knowledge_point_input,
            parent_knowledge_point: that.select_add_knowledge,
            subject: that.paper_subject
          },
          success: function (data) {
            console.log(data);
            if (data['res'] === "success") {
              console.log("添加成功");
              that.$Notice.success({
                title: '添加成功'
              });
              that.subject_change();
            }
          }
        });
      },

      // 页数发生变化
      page_change(current_page) {
        let that = this;
        console.log("页数改变", current_page, that.page_count);
        this.current_page = current_page;
        that.get_question_data(current_page, that.page_count);
      },


      // 获取制定数量的数据
      get_question_data(start_page, page_count) {
        let that = this;
        $.ajax({
          url: that.$site + "api/query_question_data",
          dataType: "json",
          data: {
            start: start_page,
            page_count: page_count
          },
          success: function (data) {
            console.log(data);
            that.data1 = data
          }
        });
      },


      // 删除指定的题目
      delete_question(question_content, question_answer, question_type, question_difficulty, paper_name) {
        console.log(question_content)
        let that = this;
        $.ajax({
          url: that.$site + "api/delete_question",
          dataType: "json",
          data: {
            question_content: question_content,
            question_answer: question_answer,
            question_type: question_type,
            question_difficulty: question_difficulty,
            paper_name: paper_name
          },
          success: function (data) {
            console.log(data);
            if (data["res"] === "success") {
              that.$Notice.success({
                title: '删除成功'
              });
              that.page_change(that.current_page);
            }
          }
        });
      },

      // 下载导入模板
      download_template() {
        this.$Modal.confirm({
          title: 'Tips',
          content: '<p>单选题多选题的选项可自由添加及删减，非选择题的选项不填即可，只填入答案</p><p>知识点请严格按照现有的知识点进行添加，每个知识点之间用中文分号；进行分隔</p>',
          onOk: () => {
            window.open('http://127.0.0.1:8000/static/TestPaperManager/excel/import_template.xlsx')
          },
          onCancel: () => {

          }
        });

      },

      //  导入试题成功
      upload_success() {
        let that = this;
        that.$Notice.success({
          title: '上传成功'
        });
        that.page_change(that.current_page);
      },

      //获取题目类型
      query_question_types(subject) {
        let that = this;
        $.ajax({
          url: that.$site + "api/query_types",
          dataType: "json",
          data: {
            subject:subject
          },
          success: function (data) {
            console.log(data);
            that.topicList = [];
            for (var i = 0; i < data.length; i++) {
              that.topicList.push({
                value: data[i]['name'],
                label: data[i]['name']
              })
            }
          }
        });
      }


    },

    mounted() {
      let that = this;
      // 路径保护
      // if (sessionStorage.getItem('per_name') == null) {
      //   this.$router.push("/")
      // } else {
      //   console.log(sessionStorage.getItem('per_name'))
      // }

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
      });


      // 获取页的总数据（30条数据为1页）
      $.ajax({
        url: that.$site + "api/query_data_count",
        dataType: "json",
        data: {},
        success: function (data) {
          console.log(data);
          that.data_count = data['count']
        }
      });

      //  获取当前页的数据
      that.get_question_data(that.current_page, that.page_count);


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
