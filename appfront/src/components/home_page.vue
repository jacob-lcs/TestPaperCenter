<template>
  <div class="all">
    <div style="text-align: right;padding-top: 10px;margin-right: 20px; font-size: 20px">
      <Poptip word-wrap content="点击登录" placement="left" trigger="hover" >
        <Icon type="ios-contact" size="40" style="margin-right: 10px; cursor: pointer"/>
      </Poptip>
    </div>
    <!--左侧信息栏-->
    <div class="sideleft">
      <p style="font-size: 35px; font-weight: bold;color: #fdfbfb">智能组卷    智慧学习</p>
      <p style="font-size: 22px;color: #fdfbfb">大数据结合试题系统 让刷题更轻松</p>
      <div style="margin-top: 30px">
        <p>轻松模板录入，提高试题更新效率。</p>
        <p>打造线上线下数字一体化。</p>
        <p>手动组卷,自动生成,试题更加个性化。</p>
        <p>服务师生，携手共进。</p>
      </div>
    </div>
    <!--  试卷导入按钮  -->
    <div style="text-align: right">
      <Card style="width:320px;" class="paper_import">
        <div style="text-align:center">
          <img src="../assets/img/paper_import.png" style="width: 100px">
          <h3 style="margin-top: 10px">试题导入</h3>
        </div>
      </Card>
      <!--  试卷导出按钮  -->
      <Card style="width:320px" class="paper_export">
        <div style="text-align:center">
          <img src="../assets/img/paper_export.png" style="width: 100px">
          <h3 style="margin-top: 10px">试卷导出</h3>
        </div>
      </Card>
    </div>
  </div>


</template>

<script>
  export default {
    name: "home_page"
  }
</script>

<style scoped>
  .all {
    background-image: url("../assets/img/bg5.jpg");
    height: 100vh;
    background-position: 50% 50%;
    background-size: 250vh;
    background-repeat: no-repeat;
  }

  .sideleft {
    color: #fdfbfb;
    width: 600px;
    height: 250px;
    float: left;
    padding: 100px 130px;
    text-align: left;
  }

  .sideleft p {
    padding: 8px 0;
    font-size: 16px;
    color: #c8cccf
  }

  .paper_import {
    width: 400px;
    height: 160px;
    background-color: rgba(255, 255, 255, 0.4);
    float: right;
    margin-right: 150px;
    margin-top: 200px;
  }

  .paper_export {
    width: 400px;
    height: 160px;
    background-color: rgba(255, 255, 255, 0.4);
    float: right;
    margin-right: 50px;
    margin-top: 200px;
  }
</style>
