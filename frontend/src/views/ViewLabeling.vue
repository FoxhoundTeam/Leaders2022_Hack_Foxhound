<template>
  <!-- панель инструментов -->
  <!-- <v-toolbar> -->
  <!-- кнопка включения простой разметки -->
  <!-- кнопка включения разметки CVAT-->
  <!-- кнопка сохранения разметки -->
  <!-- </v-toolbar> -->

  <v-row style="height: 100%" no-gutters fill-height>
    <v-col cols="12" sm="1">
      <v-card class="fill-height d-flex flex-column ma-1">
        <v-spacer vertical></v-spacer>
        <v-tooltip right>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              class="ma-1"
              tile
              elevation="0"
              outlined
              @click="onReset"
              v-bind="attrs"
              v-on="on"
            >
              <v-icon>mdi-border-radius</v-icon>
            </v-btn>
          </template>
          <span> Сброс параметров вида </span>
        </v-tooltip>

        <v-btn-toggle v-model="toggle_view" style="flex-direction: column" tile>
          <v-tooltip right>
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                class="ma-1"
                :value="'ZoomAndPan'"
                v-bind="attrs"
                v-on="on"
              >
                <v-icon>mdi-magnify</v-icon>
              </v-btn>
            </template>
            <span>
              Увеличение и пролистывание<br />
              увеличение - колесо мыши<br />
              пролистывание - зажать левую клавишу мыши и двигать курсором
            </span>
          </v-tooltip>

          <v-tooltip right>
            <template v-slot:activator="{ on, attrs }">
              <v-btn class="ma-1" :value="'Scroll'" v-bind="attrs" v-on="on">
                <v-icon>mdi-layers-triple-outline</v-icon>
              </v-btn>
            </template>
            <span>
              Пролистывание слоёв DICOM<br />
              пролистывание - зажать левую клавишу мыши и вести курсором
              вертикально<br />
              автопролистывание - двойное нажатие левой клавиши мыши
            </span>
          </v-tooltip>

          <v-tooltip right>
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                class="ma-1"
                :value="'WindowLevel'"
                v-bind="attrs"
                v-on="on"
              >
                <v-icon>mdi-brightness-6</v-icon>
              </v-btn>
            </template>
            <span>
              <p class="font-italic">Яркость и контраст<br /></p>
              <p class="font-italic">
                передвигайте мышь с зажатой левой клавишей<br />
                по горизонтали - контраст<br />
                по вертикали - яркость<br />
                двойное нажатие - автонастройка по выбранному пикселю
              </p>
            </span>
          </v-tooltip>
        </v-btn-toggle>

        <v-menu top :close-on-click="true" :nudge-width="100" offset-x>
          <template v-slot:activator="{ on: menu, attrs }">
            <v-tooltip right>
              <template v-slot:activator="{ on: tooltip }">
                <v-btn
                  class="ma-1"
                  tile
                  elevation="0"
                  outlined
                  v-bind="attrs"
                  v-on="{ ...tooltip, ...menu }"
                >
                  <v-icon>mdi-form-dropdown</v-icon>
                </v-btn>
              </template>
              Стандартные настройки яркости
            </v-tooltip>
          </template>

          <v-list dense>
            <v-list-item-group v-model="selectedStndardWindow" color="primary">
              <v-list-item v-for="(item, index) in presetNames" :key="index">
                <v-list-item-title @click="onSetPreset(item)">
                  {{ item }}
                </v-list-item-title>
              </v-list-item>
            </v-list-item-group>
          </v-list>
        </v-menu>

        <v-btn-toggle
          v-model="infoControllerVisible"
          style="flex-direction: column"
          tile
        >
          <v-tooltip right>
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                class="ma-1"
                tile
                elevation="0"
                :value="true"
                v-bind="attrs"
                v-on="on"
              >
                <v-icon>mdi-information-outline</v-icon>
              </v-btn>
            </template>
            <span
              >Включение и выключение<br />
              слоя с информацией<br />
              (в разработке)
            </span>
          </v-tooltip>
        </v-btn-toggle>

        <v-spacer vertical></v-spacer>
      </v-card>
    </v-col>
    <v-col cols="12" sm="10">
      <v-card class="fill-height d-flex flex-column ma-1">
        <!-- само поле просмотра -->
        <!-- <dwvVue /> -->
        <div id="dwv" class="ma-1">
          <!-- <md-progress-bar
            md-mode="determinate"
            :md-value="loadProgress"
          ></md-progress-bar> -->

          <!-- action buttons -->
          <!-- <div class="button-row">
            
            <md-menu md-size="medium" md-align-trigger>
              <md-button
                class="md-raised md-primary"
                md-menu-trigger
                :disabled="!dataLoaded"
              >
                {{ selectedTool }} <md-icon>arrow_drop_down</md-icon></md-button
              >
      
              <md-menu-content>
                <md-menu-item
                  v-for="tool in toolNames"
                  :key="tool"
                  v-on:click="onChangeTool(tool)"
                  >{{ tool }}</md-menu-item
                >
              </md-menu-content>
      
              <md-button
                class="md-raised md-primary"
                v-on:click="onReset()"
                :disabled="!dataLoaded"
                >Reset</md-button
              >
              <md-button
                class="md-raised md-primary"
                v-on:click="showDicomTags = true"
                :disabled="!dataLoaded"
                >Tags</md-button
              >
            </md-menu>

            <md-dialog :md-active.sync="showDicomTags">
              <tagsTable :tagsData="metaData" />
            </md-dialog>
          </div> -->

          <div id="layerGroup0" class="layerGroup">
            <!-- <div id="dropBox"></div> -->
            <div id="infoLayer">
              <div id="infotl" class="infotl info"></div>
              <div id="infotc" class="infotc infoc"></div>
              <div id="infotr" class="infotr info"></div>
              <div id="infocl" class="infocl infoc"></div>
              <div id="infocr" class="infocr infoc"></div>
              <div id="infobl" class="infobl info"></div>
              <div id="infobc" class="infobc infoc"></div>
              <!-- offset for plot -->
              <div id="infobr" class="infobr info" style="bottom: 64px"></div>
              <div id="plot"></div>
              <div id="infocm"></div>
            </div>
          </div>

          <!-- <div class="legend md-caption">
            <p>
              Powered by
              <a href="https://github.com/ivmartel/dwv" title="dwv on github">dwv</a>
              {{ versions.dwv }} and
              <a href="https://github.com/vuejs/vue" title="vue on github">Vue.js</a>
              {{ versions.vue }}
            </p>
          </div> -->
        </div>
      </v-card>
    </v-col>
    <v-col cols="12" sm="1">
      <v-card class="fill-height d-flex flex-column ma-1">
        <v-spacer vertical></v-spacer>

        <v-btn-toggle
          v-model="toggle_labeling"
          style="flex-direction: column"
          tile
        >
          <v-btn class="ma-1" :value="'Ruler'">
            <v-icon>mdi-ruler</v-icon>
          </v-btn>

          <v-btn class="ma-1" :value="'Rectangle'">
            <v-icon>mdi-vector-rectangle</v-icon>
          </v-btn>

          <v-btn class="ma-1" :value="'Roi'">
            <v-icon>mdi-vector-polygon</v-icon>
          </v-btn>

          <v-btn class="ma-1" :value="'FreeHand'">
            <v-icon>mdi-vector-radius</v-icon>
          </v-btn>

          <v-tooltip left>
            <template v-slot:activator="{ on, attrs }">
              <v-btn class="ma-1" :value="'Livewire'" v-bind="attrs" v-on="on">
                <v-icon>mdi-draw</v-icon>
              </v-btn>
            </template>
            <span>Автоконтур</span>
          </v-tooltip>
        </v-btn-toggle>

        <v-tooltip left>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              class="ma-1"
              tile
              elevation="0"
              @click="onContoursSave"
              v-bind="attrs"
              v-on="on"
            >
              <v-icon>mdi-content-save</v-icon>
            </v-btn>
          </template>
          <span>Сохранить разметку<br />на сервере</span>
        </v-tooltip>

        <v-checkbox :label="'Авто'" class="text-center"></v-checkbox>

        <v-tooltip left>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              class="ma-1"
              tile
              elevation="0"
              @click="onDownloadJsonClicked"
              v-bind="attrs"
              v-on="on"
            >
              <v-icon>mdi-download</v-icon>
            </v-btn>
          </template>
          <span>Скачать файл разметки</span>
        </v-tooltip>

        <v-tooltip left>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              class="ma-1"
              tile
              elevation="0"
              :loading="isSelecting"
              @click="handleFileImport"
              v-bind="attrs"
              v-on="on"
            >
              <v-icon>mdi-upload</v-icon>
            </v-btn>
          </template>
          <span>Загрузить файл разметки</span>
        </v-tooltip>

        <!-- компонент для загрузки файла JSON с разметкой -->
        <input
          ref="uploader"
          class="d-none"
          type="file"
          @change="onFileChanged"
        />

        <v-spacer vertical></v-spacer>

        <v-tooltip left>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              class="ma-1"
              tile
              elevation="0"
              v-bind="attrs"
              v-on="on"
              color="primary"
              disabled
            >
              <!-- <v-avatar color="primary"> -->
              <!-- <img src="https://github.com/opencv/cvat/blob/develop/site/content/en/images/logo2.png?raw=true"> -->
              <img
                width="50"
                src="https://uploads-ssl.webflow.com/62bebfb83044de7f13ae257e/62bec02423796903b293473e_Logo.svg"
              />
              <!-- </v-avatar> -->
            </v-btn>
          </template>
          <span>Экспериментальная интеграция CVAT</span>
        </v-tooltip>
      </v-card>
    </v-col>
  </v-row>
  <!-- диалог генерации -->
</template>

<script>
import http from "@/http";

import Vue from "vue";
import dwv from "dwv";

// Vue.use(MdButton);

// gui overrides

// Image decoders (for web workers)
dwv.image.decoderScripts = {
  jpeg2000: "assets/dwv/decoders/pdfjs/decode-jpeg2000.js",
  "jpeg-lossless": "assets/dwv/decoders/rii-mango/decode-jpegloss.js",
  "jpeg-baseline": "assets/dwv/decoders/pdfjs/decode-jpegbaseline.js",
  rle: "assets/dwv/decoders/dwv/decode-rle.js",
};

dwv.tool.defaultpresets = {};

dwv.tool.defaultpresets.CT = {
  mediastinum: { center: 40, width: 400 },
  lung: { center: -500, width: 1500 },
  bone: { center: 500, width: 2000 },
  brain: { center: 40, width: 80 },
  head: { center: 90, width: 350 },
};

export default {
  name: "ViewLabeling",
  components: {
    // dwvVue,
    // tagsTable,
    // Controller,
  },
  data() {
    return {
      //https://ivmartel.github.io/dwv/doc/stable/dwv.tool.html
      toggle_view: null, // состояние панели для управления видом
      toggle_labeling: null, // состояние панели для редактирования
      toggle_labeling_flag: false,
      toggle_view_flag: false,

      versions: {
        dwv: dwv.getVersion(),
        vue: Vue.version,
      },

      dwvApp: null, // библиотека DWV
      infoController: null, // оверлей с информацией о снимке
      infoControllerVisible: false, // состояние оверлея с информацией
      // standardWindows : ["Window1", "Window2", "Lung"],
      selectedStndardWindow: null,
      layergroup: null,
      viewController: null,
      presetNames: null, // пресеты по уровням яркости
      drawColor: "#FF0000",

      isSelecting: false, // для загрузки разметки в json
      selectedFile: null, // файл для загрузки разметки в json

      annotations: {}, // объекты разметки для перевода в JSON

      // номенклатура инструментов https://github.com/ivmartel/dwv-jqui/blob/master/src/applauncher.js
      tools: {
        Scroll: {},
        ZoomAndPan: {},
        WindowLevel: {},
        Draw: {
          options: ["Ruler", "Rectangle", "FreeHand", "Roi"],
          type: "factory",
          events: ["drawcreate", "drawchange", "drawmove", "drawdelete"],
        },
        Livewire: {},
      },
      toolNames: [],
      selectedTool: "Select Tool",
      loadProgress: 0,
      dataLoaded: false,
      metaData: null,
      showDicomTags: false,
      dropboxDivId: "dropBox",
      dropboxClassName: "dropBox",
      borderClassName: "dropBoxBorder",
      hoverClassName: "hover",
      file: null,
    };
  },
  methods: {
    onChangeTool: function (tool) {
      // при выборе инструмента разметки
      this.selectedTool = tool;
      this.dwvApp.setTool(tool);
      this.dwvApp.setDrawLineColour(this.drawColor);
      if (tool === "Draw") {
        this.onChangeShape(this.tools.Draw.options[0]);
        this.dwvApp.setDrawLineColour(this.drawColor); // работает на выбранном инструменте
      }
    },

    // рисование
    onChangeShape: function (shape) {
      if (this.dwvApp && this.selectedTool === "Draw") {
        this.dwvApp.setDrawShape(shape);
        this.dwvApp.setDrawLineColour(this.drawColor);
      }
    },
    onReset: function () {
      this.dwvApp.resetDisplay();
      this.dwvApp.setTool("Scroll");
      this.toggle_view_flag = true;
      this.toggle_labeling_flag = true;
      this.toggle_labeling = undefined;
      this.toggle_view = undefined;
    },
    setupDropbox() {
      this.showDropbox(true);
    },
    defaultHandleDragEvent: function (event) {
      // prevent default handling
      event.stopPropagation();
      event.preventDefault();
    },
    onBoxDragOver: function (event) {
      this.defaultHandleDragEvent(event);
      // update box border
      const box = document.getElementById(this.dropboxDivId);
      if (box && box.className.indexOf(this.hoverClassName) === -1) {
        box.className += " " + this.hoverClassName;
      }
    },
    onBoxDragLeave: function (event) {
      this.defaultHandleDragEvent(event);
      // update box class
      const box = document.getElementById(this.dropboxDivId);
      if (box && box.className.indexOf(this.hoverClassName) !== -1) {
        box.className = box.className.replace(" " + this.hoverClassName, "");
      }
    },
    onDrop: function (event) {
      this.defaultHandleDragEvent(event);
      // load files
      this.dwvApp.loadFiles(event.dataTransfer.files);
    },
    showDropbox: function (show) {
      const box = document.getElementById(this.dropboxDivId);
      if (!box) {
        return;
      }
      const layerDiv = document.getElementById("layerGroup0");

      if (show) {
        // reset css class
        box.className = this.dropboxClassName + " " + this.borderClassName;
        // check content
        if (box.innerHTML === "") {
          const p = document.createElement("p");
          p.appendChild(document.createTextNode("Drag and drop data here"));
          box.appendChild(p);
        }
        // show box
        box.setAttribute("style", "display:initial");
        // stop layer listening
        if (layerDiv) {
          layerDiv.removeEventListener("dragover", this.defaultHandleDragEvent);
          layerDiv.removeEventListener(
            "dragleave",
            this.defaultHandleDragEvent
          );
          layerDiv.removeEventListener("drop", this.onDrop);
        }
        // listen to box events
        box.addEventListener("dragover", this.onBoxDragOver);
        box.addEventListener("dragleave", this.onBoxDragLeave);
        box.addEventListener("drop", this.onDrop);
      } else {
        // remove border css class
        box.className = this.dropboxClassName;
        // remove content
        box.innerHTML = "";
        // hide box
        box.setAttribute("style", "display:none");
        // stop box listening
        box.removeEventListener("dragover", this.onBoxDragOver);
        box.removeEventListener("dragleave", this.onBoxDragLeave);
        box.removeEventListener("drop", this.onDrop);
        // listen to layer events
        if (layerDiv) {
          layerDiv.addEventListener("dragover", this.defaultHandleDragEvent);
          layerDiv.addEventListener("dragleave", this.defaultHandleDragEvent);
          layerDiv.addEventListener("drop", this.onDrop);
        }
      }
    },

    onContoursSave() {
      this.annotations = this.dwvApp.getState();
      console.log("onContoursSave(): getState = ", this.annotations);

      // this.annotations = this.dwvApp.getDrawDisplayDetails();
      // console.log("onContoursSave(): getDrawDisplayDetails = ", this.annotations);

      // var y = this.dwvApp.getDrawStoreDetails();
      // console.log("onContoursSave(): getDrawStoreDetails = ", y);
      // var json = state.toJSON(app);

      http
        .updateItem(`/api/files/${this.file.id}/markup/`, {
          data: JSON.parse(this.annotations),
          showSnackbar: true,
        })
        .then(() => {
          this.$store.commit("showSnackbar", {
            text: "Разметка успешно сохранена",
          });
        });
    },

    onSetPreset(presetname) {
      this.dwvApp.setWindowLevelPreset(presetname);
    },

    onDownloadJsonClicked() {
      // закачка файла с разметкой
      this.saveTemplateAsFile("annotations.json", this.annotations);
    },

    saveTemplateAsFile(filename, dataObjToWrite) {
      // const blob = new Blob([JSON.stringify(dataObjToWrite)], {
      const blob = new Blob([dataObjToWrite], {
        type: "text/json",
      });
      const link = document.createElement("a");

      link.download = filename;
      link.href = window.URL.createObjectURL(blob);
      link.dataset.downloadurl = ["text/json", link.download, link.href].join(
        ":"
      );

      const evt = new MouseEvent("click", {
        view: window,
        bubbles: true,
        cancelable: true,
      });

      link.dispatchEvent(evt);
      link.remove();
    },

    handleFileImport() {
      this.isSelecting = true;

      // After obtaining the focus when closing the FilePicker, return the button state to normal
      window.addEventListener(
        "focus",
        () => {
          this.isSelecting = false;
        },
        { once: true }
      );

      // Trigger click on the FileInput
      this.$refs.uploader.click();
    },

    onFileChanged(e) {
      // функция вызывается, когда файл JSON загружается на страницу
      // для восстановления разметки

      this.selectedFile = e.target.files[0];

      // Do whatever you need with the file, liek reading it with FileReader
      const file = e.target.files[0];
      console.log("selectedFile = ", file);

      let reader = new FileReader();
      reader.onload = (e) => {
        this.selectedFile = e.target.result;
        // This is a regular expression to identify carriage
        // Returns and line breaks
        // this.selectedFile = file_contents.split(/\r\n|\n/);
        console.log("split = ", this.selectedFile);
        console.log("typeof split = ", typeof this.selectedFile);
        const state = new dwv.io.State();
        console.log("state = ", state);
        // https://github.com/ivmartel/dwv/blob/develop/tests/state/state.test.js
        const jsonData = state.fromJSON(e.target.result);
        console.log("fromJSON = ", jsonData);
        state.apply(this.dwvApp, jsonData);
      };
      reader.onerror = (e) => alert(e.target.error.name);
      reader.readAsText(file);
    },
  },

  async mounted() {
    this.file = (
      await http.getItem("File", {
        id: this.$route.params.id,
        showSnackbar: true,
      })
    ).data;
    this.annotations = JSON.stringify(this.file.markup || {});
    // create app
    this.dwvApp = new dwv.App();
    console.log("mounted(): this.dwvApp = ", this.dwvApp);

    // initialise app
    this.dwvApp.init({
      dataViewConfigs: { "*": [{ divId: "layerGroup0" }] },
      tools: this.tools,
    });

    // handle load events
    let nLoadItem = null;
    let nReceivedError = null;
    let nReceivedAbort = null;
    let isFirstRender = null;
    this.dwvApp.addEventListener("loadstart", (event) => {
      // reset flags
      this.dataLoaded = false;
      nLoadItem = 0;
      nReceivedError = 0;
      nReceivedAbort = 0;
      isFirstRender = true;
      // hide drop box
      this.showDropbox(false);
      if (event.loadtype === "image") {
        // this.infoController.onLoadStart();
      }
    });
    this.dwvApp.addEventListener("loadprogress", (event) => {
      this.loadProgress = event.loaded;
    });
    this.dwvApp.addEventListener("renderend", (/*event*/) => {
      if (isFirstRender) {
        isFirstRender = false;
        // available tools
        this.toolNames = [];
        for (const key in this.tools) {
          if (
            (key === "Scroll" && this.dwvApp.canScroll()) ||
            (key === "WindowLevel" && this.dwvApp.canWindowLevel()) ||
            (key !== "Scroll" && key !== "WindowLevel")
          ) {
            this.toolNames.push(key);
          }
        }
        this.onChangeTool(this.toolNames[0]);
        console.log("mounted(): toolNames = ", this.toolNames);
      }
    });
    this.dwvApp.addEventListener("load", (/*event*/) => {
      // set dicom tags
      this.metaData = dwv.utils.objectToArray(this.dwvApp.getMetaData(0));
      // set data loaded flag
      this.dataLoaded = true;
    });
    this.dwvApp.addEventListener("loadend", (/*event*/) => {
      if (nReceivedError) {
        this.loadProgress = 0;
        // alert("Received errors during load. Check log for details.");
        // show drop box if nothing has been loaded
        if (!nLoadItem) {
          // this.showDropbox(true);
        }
      }
      if (nReceivedAbort) {
        this.loadProgress = 0;
        alert("Load was aborted.");
        // this.showDropbox(true);
        // TODO здесь подгрузка JSON разметки из БД
      }

      this.layergroup = this.dwvApp.getActiveLayerGroup();
      this.viewController = this.layergroup
        .getActiveViewLayer()
        .getViewController();
      this.presetNames = this.viewController.getWindowLevelPresetsNames();

      console.log("layer group = ", this.layergroup);
      console.log("viewController = ", this.viewController);
      console.log("presetNames = ", this.presetNames);

      const state = new dwv.io.State();
      const jsonData = state.fromJSON(this.annotations);
      state.apply(this.dwvApp, jsonData);
      this.dwvApp.resetDisplay();
      // dwv.setDrawLineColour('Red');
      // console.log("layer group = ", this.dwvApp.getActiveLayerGroup());
    });
    this.dwvApp.addEventListener("loaditem", (event) => {
      ++nLoadItem;
      if (event.loadtype === "image") {
        //
      }
    });
    this.dwvApp.addEventListener("error", (/*event*/) => {
      console.error("load error", event);
      ++nReceivedError;
    });
    this.dwvApp.addEventListener("abort", (/*event*/) => {
      ++nReceivedAbort;
    });

    // handle key events
    this.dwvApp.addEventListener("keydown", (event) => {
      this.dwvApp.defaultOnKeydown(event);
    });
    // handle window resize
    window.addEventListener("resize", this.dwvApp.onResize);

    // setup drop box
    // this.setupDropbox() // ИЗМЕНЕНО - отключил ручное перетаскивание

    // possible load from location
    dwv.utils.loadFromUri(window.location.href, this.dwvApp);
    console.log("dwv = ", dwv);
    console.log("dwvApp = ", this.dwvApp);
    this.dwvApp.loadURLs(this.file.paths);
  },
  computed: {},
  watch: {
    toggle_view: function (tool) {
      if (this.toggle_view_flag) {
        this.toggle_view_flag = false;
        return;
      }
      console.log("toggle_view changed, arg=", tool);
      if (tool == undefined) {
        // this.dwvApp.setTool('Scroll');
        this.selectedTool = "Scroll";
        return;
      }
      this.selectedTool = tool;
      this.dwvApp.setTool(tool);
      this.toggle_labeling = undefined; //TODO
      this.toggle_labeling_flag = true;
    },

    toggle_labeling: function (shape) {
      // при выборе инструмента разметки

      if (this.toggle_labeling_flag) {
        this.toggle_labeling_flag = false;
        return;
      }
      console.log("toggle_labeling changed, tool=", shape);

      // нажата кнопка сброса
      if (shape == undefined) {
        // this.dwvApp.setTool('Scroll');
        this.selectedTool = "Scroll";
        return;
      }
      // this.dwvApp.setTool('Draw');
      // this.dwvApp.setDrawShape(shape)

      //деактивация противоположной панели
      this.toggle_view = undefined; //TODO
      this.toggle_view_flag = true;

      if (shape === "Livewire") {
        this.selectedTool = "Livewire";
        this.dwvApp.setTool("Livewire");
        this.dwvApp.setDrawLineColour(this.drawColor);
        return;
      }

      // активация команды
      console.log("1. before selectedTool");
      this.selectedTool = "Draw";
      this.dwvApp.setTool("Draw");
      console.log("toggle_labeling(), shape = ", shape);
      console.log("3. onChangeShape");
      this.onChangeShape(shape);
    },

    // selectedTool:{
    //   handler(newTool){
    //     this.dwvApp.setTool(newTool);
    //     console.log("2. setTool")
    //   },
    //   immediate: true,
    // },
  },
  computed: {},
};
</script>

<!-- <style scoped>
.v-btn-toggle {
  flex-direction: column;
}
</style> -->

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#dwv {
  /*font-family: Arial, Helvetica, sans-serif;*/
  height: 100%;
  /*width: 100%;
  border: 3px;
  border-color: lightgrey;*/
}

.button-row {
  text-align: center;
  padding: 5px;
}

#dwv button {
  margin: 2px;
}

/* Layers */
.layerGroup {
  position: relative;
  padding: 0;
  display: flex;
  justify-content: center;
  height: 95%;
}
.layer {
  position: absolute;
  pointer-events: none;
}

/* drag&drop */
.dropBox {
  margin: auto;
  text-align: center;
  vertical-align: middle;
  width: 50%;
  height: 75%;
}
.dropBoxBorder {
  border: 5px dashed rgba(68, 138, 255, 0.38);
}
.dropBoxBorder.hover {
  border: 5px dashed var(--md-theme-default-primary);
}

.md-dialog {
  width: 80%;
  height: 90%;
}

/* Info */
#infoLayer {
  position: absolute;
  pointer-events: none;
  z-index: 20;
  width: 100%;
  height: 100%;
}
#infoLayer ul {
  margin: 0;
  padding: 2px;
  list-style-type: none;
}
#infoLayer li {
  margin-top: 0;
}
#infoLayer canvas {
  margin: 0;
  padding: 2px;
}
.info {
  color: #cde;
  text-shadow: 1px 1px #000;
  font-size: 80%;
}
.infoc {
  color: #ff0;
  text-shadow: 1px 1px #000;
  font-size: 120%;
}
.infotl {
  position: absolute;
  top: 0;
  left: 0;
  text-align: left;
}
.infotc {
  position: absolute;
  top: 0;
  left: 50%;
  right: 50%;
  text-align: center;
}
.infotr {
  position: absolute;
  top: 0;
  right: 0;
  text-align: right;
}
.infocl {
  position: absolute;
  bottom: 50%;
  left: 0;
  text-align: left;
}
.infocr {
  position: absolute;
  bottom: 50%;
  right: 2px;
  text-align: right;
}
.infobl {
  position: absolute;
  bottom: 0;
  left: 0;
  text-align: left;
}
.infobc {
  position: absolute;
  bottom: 0;
  left: 50%;
  right: 50%;
  text-align: center;
}
.infobr {
  position: absolute;
  bottom: 0;
  right: 0;
  text-align: right;
}

#plot {
  position: absolute;
  width: 100px;
  height: 50px;
  bottom: 15px;
  right: 0;
}
#infocm {
  position: absolute;
  bottom: 5px;
  right: 0;
}
</style>
<!-- non "scoped" style -->
<style>
.layer {
  position: absolute;
  pointer-events: none;
}
</style>
