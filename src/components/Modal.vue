<!-- ref. https://getbootstrap.jp/docs/5.3/components/modal/ -->
<!-- usage.
<script setup lang="ts">
import { ref } from "vue";
import Modal from "./Modal.vue";
const modal = ref();

modal.value.show("Header", "Body", "AcationName", () => { ... });
</script>

<template>
  <Modal ref="modal" />
  ...
</template> 
-->
<script setup lang="ts">
import { Modal } from "bootstrap";
import { ref } from "vue";

const modal = ref();
const actionButton = ref();
const _header = ref("");
const _body = ref("");
const _actionName = ref("");

// イベントを匿名関数にするとremoveEventListenerができず以前のイベントが再発火する仕様
// https://developer.mozilla.org/ja/docs/Web/API/EventTarget/addEventListener
// それを避けるためにリスナー関数を実装。それに伴う各処理の変数化
let actionDelegete: Function;
let modalObject: Modal | null = null;
function modalActionAndHide() {
  actionDelegete();
  modalObject?.hide();
}

function show(header: string, body: string, actionName: string, action: Function) {
  // UIに文字列を設定
  _header.value = header;
  _body.value = body;
  _actionName.value = actionName;

  // アクションボタンに処理を割り当てる
  actionButton.value.removeEventListener("click", modalActionAndHide); // 登録済みのイベントの削除
  actionDelegete = action;
  if (!modalObject) {
    modalObject = new Modal(modal.value);
  }
  actionButton.value.addEventListener("click", modalActionAndHide);

  // モーダル表示
  modalObject.show();
}

defineExpose({ show });
</script>

<template>
  <div ref="modal" class="modal fade" tabindex="-1" aria-labelledby="modalTitle" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <span class="modal-title fw-bold fs-5">{{ _header }}</span>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" />
        </div>
        <div class="modal-body text-center">
          <span>{{ _body }}</span>
        </div>
        <div class="modal-footer d-flex justify-content-center">
          <button ref="actionButton" class="btn btn-danger">
            <span>{{ _actionName }}</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
