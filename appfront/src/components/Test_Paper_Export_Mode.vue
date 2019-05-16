<template>
  <Row type="flex" class="height100" align="middle" justify="center" style="background-color: #eeeeee">
    <Col span="7">
      <Card class="card-button" >
        <div style="text-align:center" @click="export_byhands">
          <Icon size="200" type="md-hand"/>
          <h1>手动组卷</h1>
        </div>
      </Card>
    </Col>
    <Col span="7" >
      <Card class="card-button" >
        <div style="text-align:center" @click="export_byhands">
          <Icon size="200" type="md-color-wand"/>
          <h1>自动组卷</h1>
        </div>
      </Card>
    </Col>
  </Row>
</template>

<script>
  export default {
    name: "Test_Paper_Export_Mode",
    methods:{
      export_byhands(){
        console.log("dwhiadoaw  ");
        this.$router.push("/Test_Paper_Export_Byhands");
      },
      export_auto(){
        console.log("dwhiadoaw  ");
        this.$router.push("/Test_Paper_Export_Byhands");
      }
    }
  }
</script>

<style>
  .height100 {
    height: 100%;
  }

  #app,
  html,
  body,
  .main,
  .demo-split {
    height: 100%;
  }

  .card-button {
    width: 340px;
    height: 340px;
    margin: 0 auto;
    cursor: pointer;
    padding: 30px;
  }

</style>
