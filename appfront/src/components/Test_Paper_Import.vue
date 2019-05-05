<template>
  <div>

    <!--  添加试题dialog  -->
    <Modal v-model="modal12" draggable scrollable title="创建试题" width="90vw">

      <p slot="header" style="text-align:center">
        <Icon type="ios-download-outline"></Icon>
        <span>添加试题</span>
      </p>
      <div>
        <!--  题型选择器  -->
        <Select v-model="topic" style="width:200px" @on-change="topic_change" transfer="true" placeholder="请选择题目类型">
          <Option v-for="item in topicList" :value="item.value" :key="item.value">{{ item.label }}</Option>
        </Select>
        <!--  试题难度选择器  -->
        <Select v-model="question_difficulty" style="width:200px" transfer="true" placeholder="请选择试题难度">
          <Option v-for="item in question_difficulty_list" :value="item.value" :key="item.value">{{ item.label }}
          </Option>
        </Select>
        <br>
        <!--    试卷信息输入    -->
        <div style="margin-top: 15px; text-align: center">
          <Input size="large" v-model="paper_name" placeholder="请输入试卷名称" style="width: 300px;"/>
          <Input size="large" v-model="paper_year" placeholder="请输入试卷年份" style="width: 300px;margin-left:20px"/>
          <Input size="large" v-model="paper_subject" placeholder="请输入科目" style="width: 300px;margin-left:20px"/>

        </div>
        <!--  单选题  -->
        <div v-if="topic === '单选题'">
          <!--     知识点标签     -->
          <Tag v-for="item in knowledgepoint_list" :key="item" :name="item" closable @on-close="knowledgepoint_close">
            标签{{ item + 1 }}
            <Cascader :data="knowledge" :render-format="format"></Cascader>
          </Tag>
          <!--     输入题干     -->
          <mavon-editor v-model="single_choice_content" ref=md @imgAdd="$imgAdd" @imgDel="$imgDel"
                        placeholder="请输入题干...." style="margin-top: 15px"></mavon-editor>
          <Divider>选项</Divider>

          <!--     选择题选项    -->
          <div v-for="select_option in select_options">
            <mavon-editor v-model="select_option.content" ref=md @imgAdd="$imgAdd" @imgDel="$imgDel"
                          placeholder="请输入选项内容...." style="margin-top: 15px"></mavon-editor>
          </div>

          <!--     添加和删除选项     -->
          <div style="margin-top: 15px">
            <Button shape="circle" icon="md-add" type="primary" @click="add_select_option">添加选项</Button>
            <Button shape="circle" icon="md-close" type="error" @click="delete_select_option">删除选项</Button>
          </div>
        </div>
      </div>
      <div slot="footer" style="text-align: center;">
        <Button type="primary" icon="md-document">保存</Button>
        <Button icon="md-folder">保存并关闭</Button>
        <Button icon="md-flash">保存并新增</Button>
        <Button type="error" icon="ios-close">关闭</Button>
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

  export default {
    name: "Test_Paper_Import",
    data() {
      return {
        importpaper_flag: false,  // 导入试题dialog显示标志位
        paper_name: '',  // 试卷名称
        paper_year: '',  // 试卷年份
        paper_subject: '', // 试卷科目
        modal12: false,  // 导入试题对话框显示标志位
        topicList: [],  // 可供选择的题型
        topic: '',  //目前选择的题型
        single_choice_content: '',  // 单选题题干
        columns1: [    // 列名
          {
            title: 'Name',
            key: 'name',
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
            title: 'Age',
            key: 'age'
          },
          {
            title: 'Address',
            key: 'address'
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
        data1: [    // 数据
          {
            name: 'John Brown',
            age: 18,
            address: 'New York No. 1 Lake Park',
            date: '2016-10-03'
          },
          {
            name: 'Jim Green',
            age: 24,
            address: 'London No. 1 Lake Park',
            date: '2016-10-01'
          },
          {
            name: 'Joe Black',
            age: 30,
            address: 'Sydney No. 1 Lake Park',
            date: '2016-10-02'
          },
          {
            name: 'Jon Snow',
            age: 26,
            address: 'Ottawa No. 2 Lake Park',
            date: '2016-10-04'
          }
        ],
        select_options: [],  // 选择题选项
        question_difficulty: '',  // 题目难度
        question_difficulty_list: [],  // 题目难度列表
        knowledgepoint_list: [],  // 题目知识点列表
        knowledge:[],  // 级联选择器的知识点列表
      }
    },
    methods: {

      // 添加选项
      add_select_option() {
        var con = {
          content: ''
        };
        this.select_options.push(con)
      },

      // 删除选项
      delete_select_option() {
        this.select_options.pop()
      },

      add_paper() {
        this.importpaper_flag = true
      }
      ,
      // 导入试题dialog点击确定触发的事件
      importpaper_ok() {
        let that = this;
        if (this.paper_name === '' || this.paper_year === '') {
          that.$Message.info('请填入选项哦')
        } else {
          $.ajax({
            url: that.$site + "api/add_paper",
            dataType: "json",
            data: {
              paper_name: that.paper_name,
              paper_year: that.paper_year,
              paper_subject: that.paper_subject
            },
            success: function (data) {
              if (data['res'] === "yes") {
                that.$Message.info('试卷已创建');
              } else {
                that.$Message.info('试卷未创建，请检查网络');
              }
            }
          })
        }

      }
      ,
      // 导入试题dialog点击取消触发的事件
      importpaper_cancel() {
        this.$Message.info('试卷未创建');
      }
      ,

      // 题型发生变化
      topic_change() {
        console.log(this.topic)
      }
      ,

      // 图片上传
      $imgAdd(pos, $file) {
        let that = this
        let file = Bmob.File($file.name, $file);
        file.save().then(res => {
          console.log(res.length);
          console.log(res);
          // 将图片链接改为图片地址
          that.$refs.md.$img2Url(pos, res[0]['url']);
        })
      },

      // 删除图片触发的操作
      $imgDel(pos, $file) {

      },

      knowledgepoint_close() {
        const index = this.knowledgepoint_list.indexOf(name);
        this.knowledgepoint_list.splice(index, 1);
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
          console.log(data)
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
