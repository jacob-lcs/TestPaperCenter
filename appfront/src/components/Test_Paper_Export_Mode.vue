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
    <Modal v-model="paperInfo" width="360">
      <p slot="header" style="color:#f60;text-align:center">
        <!-- <Icon type="ios-information-circle"></Icon> -->
        <span>请输入试卷信息</span>
      </p>
      <div style="text-align:center">
        <Form :model="formLeft" label-position="left" :label-width="100">
          <FormItem label="试卷抬头">
            <Input v-model="formLeft.input1"></Input>
          </FormItem>
          <FormItem label="学校">
            <Input v-model="formLeft.input2"></Input>
          </FormItem>
          <FormItem label="科目">
            <Input v-model="formLeft.input3"></Input>
          </FormItem>
          <FormItem label="年级">
            <Input v-model="formLeft.input4"></Input>
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
      paperInfo: false,
      modal_loading: false,
      formLeft: {},
      modal_loading:false
    };
  },
  methods: {
    export_byhands() {
      console.log("dwhiadoaw  ");
      this.paperInfo = true;
      // this.$router.push("/Test_Paper_Export_Byhands");
    },
    export_auto() {
      console.log("dwhiadoaw  ");
      this.$router.push("/Test_Paper_Export_Byhands");
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
