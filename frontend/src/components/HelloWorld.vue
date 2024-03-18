<template>
  <a-layout class="layout">
    <a-layout-content :style="{ padding: '50px' }">
      <div class="container">
        <a-typography>
          <h1 class="title">Document Question Answering</h1>
        </a-typography>
        <a-card class="form-container">
          <a-upload
            class="upload-btn"
            :before-upload="handleBeforeUpload"
            :show-upload-list="false"
            @change="handleFileUpload"
          >
            <a-button> <upload-icon /> Click to Upload </a-button>
          </a-upload>

          <!-- Text input with added margin for spacing -->
          <a-input
            type="text"
            v-model="query"
            class="query-input"
            placeholder="Enter query text"
            :style="{ marginTop: '20px' }"
          />
          <div v-if="file" class="file-name">
            <p>Uploaded File: {{ file.name }}</p>
          </div>
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
  Upload,
  message,
} from "ant-design-vue";
import { UploadOutlined } from "@ant-design/icons-vue";

export default {
  name: "DocumentQuestionAnswering",
  components: {
    "a-layout": Layout,
    "a-layout-content": Layout.Content,
    "a-typography": Typography,
    "a-card": Card,
    "a-upload": Upload,
    "a-button": Button,
    "a-input": Input,
    "upload-icon": UploadOutlined,
  },

  data() {
    return {
      file: null,
      query: "",
      apiResponse: null,
    };
  },
  methods: {
    handleBeforeUpload() {
      this.file = null;
      return true;
    },
    handleFileUpload(info) {
      console.log(info);
      this.file = info.file;
    },
    async submitData() {
      if (!this.file) {
        message.error("Please select a file.");
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
        message.success("Data submitted successfully.");
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
  margin-top: 20px; /* Added margin for spacing */
}

.submit-button {
  width: 100%;
  margin-top: 20px; /* Added margin for spacing */
}

.response {
  background-color: #f0f0f0;
  border-radius: 4px;
  padding: 15px;
}

.upload-btn {
  margin-bottom: 20px; /* Added margin for spacing */
}
</style>
