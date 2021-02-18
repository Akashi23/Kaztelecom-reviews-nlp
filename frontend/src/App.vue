<template>
  <div class="wrapper-div">
    <b-card-group deck>
      <b-card
        text-variant="black"
        class="text-center shadow p-3 mb-5 bg-white rounded"
      >
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
    <b-card-group deck>
      <b-card
        text-variant="black"
        class="text-center shadow p-3 mb-5 bg-white rounded"
      >
        <div class="chart-wrapper">
          <v-chart autoresize :options="chartOptionsTextFreq"></v-chart>
        </div>
      </b-card>
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
        }
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
            type: 'bar',
            data: this.freq_text,
            emphasis: {
                itemStyle: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            }
          },
        ],
        tooltip: {
            trigger: 'item'
        },
        legend: {
            orient: 'vertical',
            left: 'left',
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
      console.log(data_rating);
      const rating = data_rating.data;
      const reaction = data_reaction.data;
      this.rating_number = rating.rating_number;
      this.rating_count = rating.rating_count;

      this.reaction_number = reaction.reaction_number;
      this.reaction_count = reaction.reaction_count;

      this.freq_text = data_text.data.word_text_freq;
      this.freq_title = data_title.data.word_title_freq;
      console.log(reaction.reaction_number);
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
.text_freq{
  color: black;
  width: 100%;
  height: 530px;
}
</style>
