<template>
  <div>
    <!--  导入试题 dialog  -->
    <Modal
      v-model="importpaper_flag"
      title="创建试题"

      @on-ok="importpaper_ok"
      :mask-closable = false
      @on-cancel="importpaper_cancel">
      <div style="text-align: center">
        <Input v-model="paper_name" placeholder="请输入试卷年份" style="width: 300px; height: 50px; margin-top: 20px"/>
        <Input v-model="paper_year" placeholder="请输入试卷名称" style="width: 300px;  height: 50px; margin-top: 20px"/>
      </div>
    </Modal>

    <div style="text-align: left; margin-top: 20px; margin-left: 50px">
      <Button type="primary" @click="add_paper">
        <Icon type="md-add"/>
        创建试卷
      </Button>
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
      }
    },
    methods: {
      add_paper() {
        this.importpaper_flag = true
      },
      // 导入试题dialog点击确定触发的事件
      importpaper_ok() {
        let that = this
        if (this.paper_name === '' || this.paper_year === '') {
          that.$Message.info('请填入选项哦')
        } else {
          $.ajax({
            url: that.$site + "api/add_paper",
            dataType: "json",
            data: {
              paper_name: that.paper_name,
              paper_year: that.paper_year
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

      },
      // 导入试题dialog点击取消触发的事件
      importpaper_cancel() {
        this.$Message.info('试卷未创建');
      }

    },
    mounted(){
      if(sessionStorage.getItem('per_name') == null){
        this.$router.push("/")
      }else {
        console.log(sessionStorage.getItem('per_name'))
      }
    }
  }
</script>

<style scoped>

</style>
