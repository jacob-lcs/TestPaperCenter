<template>
  <div class="export_all">
    <Row type="flex">
      <Col span="12" offset="2" style="margin-top: 60px">
        <Carousel autoplay autoplay-speed="2500" v-model="value2" loop>
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

      <!--    <Row-->
      <!--      type="flex"-->
      <!--      class="heightbelow"-->
      <!--      align="middle"-->
      <!--      justify="center"-->
      <!--    >-->
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
    <!-- 信息填写！ -->
    <Modal v-model="showPaperInfo" width="360">
      <p slot="header" style="color:#f60;text-align:center">
        <!-- <Icon type="ios-information-circle"></Icon> -->
        <span>请输入试卷信息</span>
      </p>
      <div style="text-align:center">
        <Form :model="paperInfo" label-position="left" :label-width="100">
          <FormItem label="试卷抬头">
            <Input v-model="paperInfo.paper_name"></Input>
          </FormItem>
          <FormItem v-if="mode==='auto'" label="总分">
            <Input v-model="paperInfo.score"></Input>
          </FormItem>
          <FormItem v-if="mode==='auto'" label="题目数量">
            <Input v-model="paperInfo.question_num"></Input>
          </FormItem>
          <FormItem label="科目">
            <Select v-model="paperInfo.subject">
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
      <div slot="footer">
        <Button type="error" size="large" long :loading="modal_loading" @click="confirm">确定</Button>
      </div>
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
      modal_loading: false,
      paperInfo: {
        paper_name: "兰生复旦7年级综合卷",
        // school: "复旦什么学校",
        subject: 1,
        grade: 1,
        score: 100,
        question_num: 10
      },
      mode: "auto",
      subjects: [],
      grades: []
    };
  },
  mounted() {
    // 路径保护
      if (sessionStorage.getItem('per_name') === null || sessionStorage.getItem('identity') === 'keyboarder') {
        this.$router.push("/")
      } else {
        console.log(sessionStorage.getItem('per_name'))
      }
    // 查询题型
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
  },
  methods: {
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
    confirm() {
      if (this.mode === "manual")
        this.$router.push({
          name: "Test_Paper_Export_Byhands",
          params: this.paperInfo
        });
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

/* .ivu-layout-content {
    position: absolute;
    top: 50px;
    bottom: 0;
    left: 0;
    width: 100%;
  } */
</style>

