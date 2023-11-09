<template>
    <div class="whole">
        <div class="title">
            <img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="125" height="125" />
        </div>
        <el-form :model="form" class="form" label-width="200px">
            <el-form-item label="修改仓库配置：">
                <el-button>修改部署配置</el-button>
                <el-button>上传配置文件</el-button>
            </el-form-item>
            <el-form-item label="添加新仓库：">
                <el-select v-model="form.region" placeholder="放哪个文件夹？">
                </el-select>
            </el-form-item>
            <el-form-item label="仓库URL：">
                <el-input placeholder="只要立哥有权限，你随便放"></el-input>
            </el-form-item>
            <el-form-item label="仓库分支：">
                <el-input placeholder="手动输入更健康"></el-input>
            </el-form-item>
            <el-form-item label="确认添加：">
                <el-button>有这闲工夫瞎点，还不如自己改配置</el-button>
            </el-form-item>
            <el-form-item label="查看仓库网页：">
                <el-select v-model="form.region" placeholder="选择你要查看的仓库名">
                </el-select>
            </el-form-item>
            <el-form-item label="仓库链接：">
                <a href="baidu.com">仓库链接</a>
            </el-form-item>
            <el-form-item label="高亮分支：">
                <el-select v-model="form.region" placeholder="右侧高亮选中分支">
                </el-select>
            </el-form-item>
            <el-form-item label="修改定时任务时间：">

            </el-form-item>
            <el-form-item label="立刻更新：">
                <el-button>立刻更新</el-button>
            </el-form-item>
            <el-form-item label="我有话想说：">
                <el-input placeholder="说吧，一个字五块钱"></el-input>
            </el-form-item>
        </el-form>
    </div>
</template>
  
<script lang="ts" setup>
import { reactive } from 'vue'

// do not use same name with ref
const form = reactive({
    name: '',
    region: '',
    date1: '',
    date2: '',
    delivery: false,
    type: [],
    resource: '',
    desc: '',
})

const onSubmit = () => {
    console.log('submit!')
}
</script>

<style scoped>
@import url('../styles/horizontal-list.css');
.logo {
  position: absolute;
  left: 10px;
  top: 10px;
  z-index: 1;
}

.form {
    display: flex;
    flex-direction: column;
    width: 100%;
}
.el-form-item {
    display: flex;
    width: 100%;
}

.el-input {
    padding-right: 30px;
}
</style>