<template>
  <a-layout class="layout">
    <a-layout-content :style="{ padding: '50px' }">
      <div class="container">
        <a-typography>
          <h1 class="title">Document Question Answering</h1>
        </a-typography>
        <a-card class="form-container">
          <a-input type="file" @change="handleFileUpload" class="input-file" />

          <a-input
            type="text"
            v-model="query"
            class="query-input"
            placeholder="Enter query text"
          />
          <a-button type="primary" @click="submitData" class="submit-button">
            Submit
          </a-button>
        </a-card>
        <a-card
          v-if="apiResponse"
          class="response-container"
          style="margin-top: 20px"
        >
          <a-typography>
            <h3 class="response-title">API Response:</h3>
          </a-typography>
          <div v-html="renderMarkdown(apiResponse)" class="response"></div>
        </a-card>
      </div>
    </a-layout-content>
  </a-layout>
</template>

<script>
import axios from "axios";
import markdownIt from "markdown-it";
import {
  Layout,
  Typography,
  Card,
  Button,
  Input,
  message,
} from "ant-design-vue";
// import { UploadOutlined } from "@ant-design/icons-vue";

export default {
  name: "DocumentQuestionAnswering",
  components: {
    "a-layout": Layout,
    "a-layout-content": Layout.Content,
    "a-typography": Typography,
    "a-card": Card,
    // "a-upload": Upload,
    "a-button": Button,
    "a-input": Input,
    // "upload-icon": UploadOutlined,
  },

  data() {
    return {
      file: null,
      query: "",
      apiResponse: null,
    };
  },
  methods: {
    handleFileUpload(event) {
      this.file = event.target.files[0];
    },
    async submitData() {
      if (!this.file) {
        alert("Please select a file.");
        return;
      }

      const formData = new FormData();
      formData.append("file", this.file);
      formData.append("query", this.query);

      try {
        const response = await axios.post(
          "http://localhost:8080/predict",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        );

        this.apiResponse = response.data.result;
      } catch (error) {
        console.error("API request failed:", error);
        message.error("Failed to get response from the API.");
        this.apiResponse = null;
      }
    },
    renderMarkdown(text) {
      const md = new markdownIt();
      return md.render(text);
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 600px;
  margin: 0 auto;
}

.title {
  text-align: center;
  margin-bottom: 20px;
}

.form-container,
.response-container {
  background: #fff;
  padding: 24px;
  border-radius: 4px;
}

.query-input {
  width: 100%;
}

.submit-button {
  width: 100%;
}

.response {
  background-color: #f0f0f0;
  border-radius: 4px;
  padding: 15px;
}
</style>
