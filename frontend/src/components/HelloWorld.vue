<template>
  <a-layout class="layout">
    <a-layout-content :style="{ padding: '50px' }">
      <div class="container" style="text-align: left">
        <a-typography>
          <h1 class="title">Document Question Answering</h1>
        </a-typography>
        <a-card>
          <a-input
            @change="updateQuery"
            class="input"
            placeholder="Enter query text"
          />
          <div v-if="file" class="file-name">
            <p>Uploaded File: {{ file.name }}</p>
          </div>
          <a-col>
            <a-upload
              class="upload-btn"
              :before-upload="handleBeforeUpload"
              :show-upload-list="false"
              @change="handleFileUpload"
            >
              <a-button type="primary" ghost>
                <upload-icon /> Click to Upload
              </a-button>
            </a-upload>
            <span>&nbsp;&nbsp;</span>
            <a-button
              type="primary"
              @click="submitData"
              class="submit-button"
              :disabled="submitting"
            >
              Submit
            </a-button>
          </a-col>

          <a-typography>
            <h3 class="response-title" style="text-align: left">Results</h3>
          </a-typography>

          <a-typography class="primary" style="font-size: 20px; width: 1200px">
            {{ apiResponse }}
          </a-typography>
        </a-card>
      </div>
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
    const submitting = ref(false);

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
      if (file.value.size > 10 * 1024 * 1024) {
        message.error("File size must be smaller than 10MB!");
        file.value = null;
      }
    };

    const updateQuery = (event) => {
      query = event.target.value;
    };

    const submitData = async () => {
      submitting.value = true;

      if (!file.value) {
        message.error("Please select a file.");
        return;
      }

      let formData = new FormData();
      formData.append("file", file.value.originFileObj);
      formData.append("query", query);

      try {
        const response = await axios.post(
          "https://ragbackend.azurewebsites.net//predict",
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
      } finally {
        submitting.value = false;
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
      submitting,
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

.input {
  margin-top: 20px;
  font-size: 30px;
}

.submit-button {
  width: 20%;
  margin-top: 20px; /* Added margin for spacing */
}

.upload-btn {
  margin-bottom: 20px; /* Added margin for spacing */
}
</style>
