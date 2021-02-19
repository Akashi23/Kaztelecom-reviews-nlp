<template>
  <div class="wrapper-div">
    <b-card-group columns>
      <b-card
        text-variant="black"
        class="text-center shadow p-3 mb-5 bg-white rounded"
      >
        <b-row>
          <b-col sm="3">
            <b-img src="https://halberdbastion.com/sites/default/files/styles/medium/public/2018-04/kazakhtelecom-logo.png?itok=Hpk1k5ZY" fluid alt="Fluid image"></b-img>
          </b-col>
          <b-col sm="8">
            <h3>Казахтелеком</h3>
            <p class="border text-justify rounded text-pad">«Казахтелеком» (каз. «Қазақтелеком»)  казахстанская телекоммуникационная компания, имеющая статус национальной компании. Является крупнейшим оператором фиксированной телефонии в Казахстане, а также одним из крупнейших операторов Национальной сети передачи данных.</p>
          </b-col>
        </b-row>
      </b-card>
      <b-card
        text-variant="black"
        class="text-center shadow p-3 mb-5 bg-white rounded"
      >
        <h3>Система определения настроя отзыва</h3>
        <br />
        <b-form-textarea
          id="textarea-auto-height"
          v-model="text_for_test"
          placeholder="Напишите свой отзыв, для определения реакции"
          rows="3"
          max-rows="8"
        ></b-form-textarea>
        <br />
        <b-button pill variant="outline-danger" v-on:click="getPrediction()"
          >Определить</b-button
        >
        <b-alert v-if="prediction === true" show variant="success mt-4">
          <h4 class="alert-heading">Определили!</h4>
          <p>
            Ваш отзыв положительный! Если ваш отзыв не положительный то машины
            тоже могут ошибаться!
          </p>
        </b-alert>
        <b-alert v-else-if="prediction === false" show variant="danger mt-4">
          <h4 class="alert-heading">Определили!</h4>
          <p>
            Ваш отзыв Отрицательный! Если ваш отзыв не отрицательный то машины
            тоже могут ошибаться!
          </p>
        </b-alert>
      </b-card>
      <b-card
        text-variant="black"
        class="text-center shadow p-3 mb-5 bg-white rounded"
      >
        <h3>Нахождение ключевых слов из частот слов</h3>
        <br />
        <b-form-tags
          input-id="tags-separators"
          v-model="keywords"
          separator=" ,;"
          placeholder="Подберите ключевые слова"
          no-add-on-enter
        ></b-form-tags>
        <br />
        <b-button pill variant="outline-primary" v-on:click="getKeywords()"
          >Найти</b-button
        >
        <br />
        <br />
        <div v-if="keywords_in_freq" class="text_freq">
          <v-chart autoresize :options="chartOptionsKeywordsPie"></v-chart>
        </div>
      </b-card>
    </b-card-group>
    <b-card-group deck>
      <b-card
        text-variant="black"
        class="text-center shadow p-3 mb-5 bg-white rounded"
      >
        <div class="chart-wrapper">
          <v-chart autoresize :options="chartOptionsTitleFreq"></v-chart>
        </div>
      </b-card>
      <b-card
        text-variant="black"
        class="text-center shadow p-3 mb-5 bg-white rounded"
      >
        <div class="chart-wrapper">
          <v-chart autoresize :options="chartOptionsRating"></v-chart>
        </div>
      </b-card>
      <b-card
        text-variant="black"
        class="text-center shadow p-3 mb-5 bg-white rounded"
      >
        <div class="chart-wrapper">
          <v-chart autoresize :options="chartOptionsReaction"></v-chart>
        </div>
      </b-card>
    </b-card-group>
    <b-card-group class="text_freq_group" deck>
      <b-card
        text-variant="black"
        class="text-center shadow p-3 mb-5 bg-white rounded"
      >
        <div class="text_freq">
          <v-chart autoresize :options="chartOptionsTextFreq"></v-chart>
        </div>
      </b-card>
    </b-card-group>
  </div>
</template>

<script>
export default {
  name: "App",
  created() {
    this.getData();
  },
  data() {
    return {
      keywords_in_freq: null,
      prediction: null,
      keywords: ["интернет"],
      text_for_test: "",
      rating_number: [],
      rating_count: [],
      reaction_number: [],
      reaction_count: [],
      freq_text: [],
      freq_title: [],
    };
  },
  computed: {
    chartOptionsRating() {
      return {
        xAxis: {
          type: "category",
          data: this.rating_number,
        },
        yAxis: {
          type: "value",
        },
        series: [
          {
            type: "bar",
            data: this.rating_count,
          },
        ],
        tooltip: {
          trigger: "axis",
        },
        title: { text: "Рейтинги из обзоров" },
        color: ["#ff6666", "#ff9999"],
        animationDelay: function (idx) {
          return idx * 5;
        },
      };
    },
    chartOptionsReaction() {
      return {
        xAxis: {
          type: "category",
          data: this.reaction_number,
        },
        yAxis: {
          type: "value",
        },
        series: [
          {
            type: "bar",
            data: this.reaction_count,
          },
        ],
        tooltip: {
          trigger: "axis",
        },
        title: { text: "Реакция из обзоров" },
        color: ["#66b3ff", "#3399ff"],
      };
    },
    chartOptionsTextFreq() {
      return {
        xAxis: {
          type: "category",
          axisLabel: { interval: 0, rotate: 30 },
        },
        yAxis: {
          type: "value",
        },
        series: [
          {
            type: "bar",
            data: this.freq_text,
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: "rgba(0, 0, 0, 0.5)",
              },
            },
          },
        ],
        tooltip: {
          trigger: "item",
        },
        legend: {
          orient: "vertical",
          left: "left",
        },
        title: { text: "Частота слов из текста обзоров" },
        color: ["#ff6666", "#ff9999"],
      };
    },
    chartOptionsTitleFreq() {
      return {
        xAxis: {
          type: "category",
        },
        yAxis: {
          type: "value",
        },
        series: [
          {
            type: "bar",
            data: this.freq_title,
          },
        ],
        tooltip: {
          trigger: "axis",
        },
        title: { text: "Частота слов из титула обзоров" },
        color: ["#66b3ff", "#3399ff"],
      };
    },

    chartOptionsKeywordsPie() {
      return {
        title: {
          text: "Ключевые слова с частотами из частот слов ",
          left: "center",
        },
        tooltip: {
          trigger: "item",
          formatter: "{a} <br/>{b} : {c} ({d}%)",
        },
        legend: {
          orient: "vertical",
          left: "left",
        },
        series: [
          {
            name: "Ключевое слово",
            type: "pie",
            radius: "50%",
            data: this.keywords_in_freq,
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: "rgba(0, 0, 0, 0.5)",
              },
            },
          },
        ],
      };
    },
  },
  methods: {
    async getData() {
      const data_rating = await this.axios.get(
        "http://localhost:3000/features/?select=rating"
      );
      const data_reaction = await this.axios.get(
        "http://localhost:3000/features/?select=reaction"
      );
      const data_text = await this.axios.get(
        "http://localhost:3000/features/?select=freq,text"
      );
      const data_title = await this.axios.get(
        "http://localhost:3000/features/?select=freq,title"
      );
      const rating = data_rating.data;
      const reaction = data_reaction.data;
      this.rating_number = rating.rating_number;
      this.rating_count = rating.rating_count;

      this.reaction_number = reaction.reaction_number;
      this.reaction_count = reaction.reaction_count;

      this.freq_text = data_text.data.word_text_freq;
      this.freq_title = data_title.data.word_title_freq;
    },
    async getKeywords() {
      var str = this.keywords.join(",");
      const data_keywords = await this.axios.get(
        `http://localhost:3000/keywords/?keywords=${str}`
      );
      let label = data_keywords.data.Label;
      let count = data_keywords.data.Count;
      let label_array = [];
      let count_array = [];
      let keywords_for_save = [];
      Object.keys(label).map((key) => label_array.push(label[key]));
      Object.keys(count).map((key) => count_array.push(count[key]));
      for (let i = 0; i <= label_array.length; i++) {
        let dict = {
          value: count_array[i],
          name: label_array[i],
        };
        keywords_for_save.push(dict);
      }
      this.keywords_in_freq = keywords_for_save;
    },
    async getPrediction() {
      const data_prediction = await this.axios.post(
        "http://localhost:3000/predict",
        { text: this.text_for_test }
      );
      this.prediction = Boolean(data_prediction.data);
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.echarts {
  color: black;
  width: 100%;
  height: 100%;
}
.chart-wrapper {
  color: black;
  width: 100%;
  height: 430px;
}
.wrapper-div {
  margin: 20px;
}
.card-body {
  padding: 0px;
}
.text_freq {
  color: black;
  width: 100%;
  height: 530px;
}
.text-pad{
  padding: 20px;
}
</style>
