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
          <a-textarea
            @change="updateQuery"
            class="textarea"
            placeholder="Enter query text"
            :style="{ marginTop: '20px' }"
            :rows="4"
          />
          <div v-if="file" class="file-name">
            <p>Uploaded File: {{ file.name }}</p>
          </div>
          <a-button type="primary" @click="submitData" class="submit-button">
            Submit
          </a-button>
        </a-card>
      </div>

      <a-typography>
        <h3 class="response-title">API Response:</h3>
      </a-typography>
      <a-card
        class="response-container"
        v-if="apiResponse"
        style="margin-top: 20px; width: 1400px; word-wrap: break-word"
      >
        <a-typography class="primary">
          {{ apiResponse }}
        </a-typography>
      </a-card>
    </a-layout-content>
  </a-layout>
</template>

<script>
import { ref } from "vue";
import axios from "axios";
import markdownIt from "markdown-it";
import {
  Layout,
  Typography,
  Card,
  Button,
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
    "upload-icon": UploadOutlined,
  },

  setup() {
    const file = ref(null);
    let query = "query 1";
    const apiResponse = ref(null);

    const handleBeforeUpload = () => {
      file.value = null;
      return true;
    };

    const handleFileUpload = (info) => {
      console.log(info);
      file.value = info.file;
      // Check if the file if pdf
      if (file.value.type !== "application/pdf") {
        message.error("Please upload a PDF file.");
        file.value = null;
      }

      // Check if file is under 100MB
      if (file.value.size > 100 * 1024 * 1024) {
        message.error("File size must be smaller than 100MB!");
        file.value = null;
      }
    };

    const updateQuery = (event) => {
      query = event.target.value;
    };

    const submitData = async () => {
      if (!file.value) {
        message.error("Please select a file.");
        return;
      }

      let formData = new FormData();
      formData.append("file", file.value.originFileObj);
      formData.append("query", query);

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

        apiResponse.value = response.data.result;
        message.success("Data submitted successfully.");
      } catch (error) {
        console.error("API request failed:", error);
        message.error("Failed to get response from the API.");
        apiResponse.value = null;
      }
    };

    const renderMarkdown = (text) => {
      const md = new markdownIt();
      return md.render(text);
    };

    return {
      file,
      query,
      apiResponse,
      updateQuery,
      handleBeforeUpload,
      handleFileUpload,
      submitData,
      renderMarkdown,
    };
  },
};
</script>

<style scoped>
.container {
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
  width: 20%;
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
