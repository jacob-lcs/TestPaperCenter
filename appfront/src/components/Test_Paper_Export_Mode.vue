<template>
  <Row
    type="flex"
    class="height100"
    align="middle"
    justify="center"
    style="background-color: #eeeeee"
  >
    <Col span="7">
      <Card class="card-button">
        <div style="text-align:center" @click="export_byhands">
          <Icon size="200" type="md-hand"/>
          <h1>手动组卷</h1>
        </div>
      </Card>
    </Col>
    <Col span="7">
      <Card class="card-button">
        <div style="text-align:center" @click="export_byhands">
          <Icon size="200" type="md-color-wand"/>
          <h1>自动组卷</h1>
        </div>
      </Card>
    </Col>
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
          <FormItem label="学校">
            <Input v-model="paperInfo.school"></Input>
          </FormItem>
          <FormItem label="科目">
            <Select v-model="paperInfo.subject">
              <Option value="1" key="1">数学</Option>
              <Option value="2" key="2">物理</Option>
            </Select>
          </FormItem>
          <FormItem label="年级" style="margin-bottom:0px">
            <Select v-model="paperInfo.grade">
              <Option value="1" key="1">初中一年级</Option>
              <Option value="2" key="2">初中二年级</Option>
            </Select>
          </FormItem>
        </Form>
      </div>
      <div slot="footer">
        <Button type="error" size="large" long :loading="modal_loading" @click="confirm">确定</Button>
      </div>
    </Modal>
  </Row>
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
        school: "复旦什么学校",
        subject: "1",
        grade: "2"
      },
      modal_loading: false,
      mode: "auto"
    };
  },
  methods: {
    export_byhands() {
      console.log("manual");
      this.mode = "manual";
      this.showPaperInfo = true;
      this.$router.push({
        name: "Test_Paper_Export_Byhands",
        params: this.paperInfo
      });
    },
    export_auto() {
      console.log("auto");
      this.mode = "auto";
      this.showPaperInfo = true;
      // this.$router.push("/Test_Paper_Export_Byhands");
    },
    confirm() {
      this.modal_loading = true;
      setTimeout(() => {
        this.modal_loading = false;
        this.modal2 = false;
        this.$Message.success("Successfully delete");
      }, 2000);
    }
  }
};
</script>

<style scope>
.height100 {
  height: 100%;
}

.card-button {
  width: 340px;
  height: 340px;
  margin: 0 auto;
  cursor: pointer;
  padding: 30px;
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
