<template>
  <Vueform
    size="md"
    :endpoint="false"
    validate-on="step"
    :float-placeholders="false"
    add-class="vf-application-form"
    ref="form$"
    @submit="handleSubmit"
    @mounted="onFormMounted"
    @change="updateData"
  >
    <template #empty>
      <FormSteps>
        <FormStep
          name="page0"
          :elements="[
            'register_title',
            'h2_4',
            'h3_9',
            'p_7',
            'h3_7',
            'p_2',
            'h3_8',
            'p_6',
            'h3_10',
            'p_8',
            'divider',
            'checkbox',
          ]"
          label="开始"
        />
        <FormStep
          name="page1"
          :elements="[
            'h2',
            'h3',
            'name',
            'wxid',
            'sex',
            'school',
            'email',
            'grade',
            'divider_1',
            'h3_1',
            'p',
            'mbti_ei',
            'mbti_sn',
            'mbti_tf',
            'mbti_jp',
            'divider_2',
          ]"
          label="关于你"
        />
        <FormStep
          name="page2"
          :elements="[
            'h2_1',
            'hobbies',
            'travel_destination',
            'superpower',
            'use_of_money',
            'family',
            'lifestyle',
            'divider_3',
          ]"
          label="更多"
        />
        <FormStep
          name="page3"
          label="关于ta"
          :elements="[
            'h2_2',
            'h3_2',
            'p_1',
            'preferred_sex',
            'preferred_grades',
            'preferred_schools',
            'divider_4',
            'h3_3',
            'p_3',
            'radioTabs',
            'preferred_mbti_ei',
            'preferred_mbti_sn',
            'preferred_mbti_tf',
            'preferred_mbti_jp',
            'divider_6',
            'h3_4',
            'preferred_wxid',
            'continue_match',
            'divider_5',
          ]"
        />
        <FormStep
          name="page4"
          label="结束"
          :elements="[
            'h2_3',
            'h3_11',
            'p_4',
            'h3_5',
            'p_5',
            'divider_7',
            'h3_6',
            'comment',
            'confirm1',
            'confirm2',
            'divider_8',
          ]"
        />
      </FormSteps>

      <FormElements>
        <StaticElement
          name="register_title"
          tag="h1"
          content="Triple Uni 一周CP 2025 活动报名问卷"
        />
        <StaticElement
          name="h2_4"
          tag="h2"
          content="活动须知  (请全部阅读)"
          top="1"
        />
        <StaticElement name="h3_9" tag="h3" content="形式" top="1" />
        <StaticElement
          name="p_7"
          tag="p"
          content="<div><strong>本次活动为半自助形式, 参与者需要访问本网址 (valentine.tripleuni.com)&nbsp; 获取匹配结果, 查看、提交每日任务等...</strong><br><br>匹配成功的小组会被分配一个Mentor, ta的联系方式将在本网站展示, 请参与者主动添加Mentor缴纳押金, 在活动过程中如有疑问或遇到问题都可以与Mentor联系.</div>"
        />
        <StaticElement name="h3_7" tag="h3" content="时间线" top="2" />
        <StaticElement
          name="p_2"
          tag="p"
          content="<div>2.1 19:00 开始报名<br>2.4 10:00 截止报名<br>2.4 19:00 公布第一轮匹配结果<br><strong>2.5 23:59 第一轮确认&amp;押金缴纳ddl<br></strong>2.6 08:00 公布第二轮匹配结果<br><strong>2.7 12:00 第二轮确认&amp;押金缴纳ddl<br></strong>2.7 22:00 双方可查看对方微信号并自主添加<br>2.8 00:00 第一天任务公布, 活动正式开始<br>...<br>2:14 23:59 第七天任务提交ddl, 活动结束<br><br>第一轮匹配未成功的申请人将会参与第二轮匹配, 请及时查看结果</div>"
        />
        <StaticElement name="h3_8" tag="h3" content="押金缴纳流程" top="2" />
        <StaticElement
          name="p_6"
          tag="p"
          content="<div>匹配结果公布后, 参与者需要在对应轮次的押金缴纳ddl前添加Mentor微信并缴付押金 70 元人民币. 在付款后Mentor将会提供一个二维码, 扫描后转跳本网站并显示押金缴付成功. <br><br>若申请人未能在对应轮次的ddl前缴纳押金, 匹配将会作废且申请人将<strong>不能</strong>参与下一轮次的匹配.&nbsp;</div>"
        />
        <StaticElement
          name="h3_10"
          tag="h3"
          content="数据收集 & 隐私承诺"
          top="2"
        />
        <StaticElement
          name="p_8"
          tag="p"
          content="<div>出于匹配目的, 我们将会收集并保存以下隐私信息:<br><br>[通过微信登陆授权]<br>你的微信头像<br>你的微信昵称<br>你的微信OpenID (用作网站登陆)<br><br>[通过填写问卷]<br>所有在问卷中填写的所有内容<br><br><strong>我们承诺将尽最大努力妥善保管你的隐私数据, 秉承最小权限原则限制他人不必要的访问.&nbsp;<br><br>我们承诺不会将这些数据提供给任何无关第三方.<br></strong><br></div>"
        />
        <StaticElement name="divider" tag="hr" top="2" />
        <CheckboxElement
          name="checkbox"
          field-name="规则及隐私条款"
          :rules="['accepted']"
          text="我已详细阅读并理解以上所有内容并且同意押金缴纳规则及隐私政策。"
          :submit="false"
        />

        <StaticElement name="h2" tag="h2" content="个人信息" />
        <StaticElement name="h3" tag="h3" content="基础信息" />
        <TextElement
          name="name"
          field-name="姓名"
          label="你的姓名"
          placeholder="张三"
          :rules="['required', 'max:4']"
        />
        <TextElement
          name="wxid"
          field-name="微信号"
          :columns="{
            label: 12,
            wrapper: 12,
          }"
          :rules="['required', 'max:50']"
          label="你的微信"
          description="请确定wxid正确，且可被搜索/ 添加。如果您的微信号是以wxid开头的原始id，请填入电话号。"
          placeholder="my_wechat_id"
        />
        <RadiogroupElement
          name="sex"
          field-name="性别"
          view="tabs"
          :items="[
            {
              value: 'M',
              label: '男',
            },
            {
              value: 'F',
              label: '女',
            },
          ]"
          label="你的性别"
          :rules="['required']"
        />
        <RadiogroupElement
          name="school"
          field-name="就读学校"
          view="blocks"
          :items="[
            {
              value: 'HKU',
              label: 'HKU',
              description: '',
            },
            {
              value: 'CUHK',
              label: 'CUHK',
              description: '',
            },
            {
              value: 'UST',
              label: 'HKUST',
              description: null,
            },
          ]"
          label="你就读的学校"
          :rules="['required']"
        />
        <TextElement
          name="email"
          input-type="email"
          :rules="[
            'nullable',
            'required',
            'regex:^[a-zA-Z0-9._%+-]+@(connect\\.ust\\.hk|connect\\.hku\\.hk|link\\.cuhk\\.edu\\.hk)$',
            'email',
          ]"
          label="你的学校邮箱"
          placeholder="example@example.com"
          info="我们可能会发送验证码至此邮箱以验证归属"
        />
        <RadiogroupElement
          name="grade"
          field-name="年级"
          view="blocks"
          :items="[
            {
              value: 'UG1',
              label: '本科大一',
              description: null,
            },
            {
              value: 'UG2',
              label: '本科大二',
              description: null,
            },
            {
              value: 'UG3',
              label: '本科大三',
              description: null,
            },
            {
              value: 'UG4',
              label: '本科大四',
              description: null,
            },
            {
              value: 'UG5',
              label: '本科大五',
              description: null,
            },
            {
              value: 'PG',
              label: '硕/博士生',
              description: null,
            },
            {
              value: 'PROF',
              label: '教授',
              description: null,
            },
          ]"
          label="你目前的年级"
          :rules="['required']"
        />
        <StaticElement name="divider_1" tag="hr" top="1" bottom="1" />
        <StaticElement name="h3_1" tag="h3" content="MBTI 性格测试结果" />
        <StaticElement
          name="p"
          tag="p"
          content="<div>请通过滑动的方式选择你的MBTI.<br><br>如果你不确定自己的MBTI, 可以通过 <a href='https://www.16personalities.com\' target='blank'>https://www.16personalities.com</a><br>或其他网站进行测试.<br><br>如果你只知道自己的MBIT而不确定具体的百分比, 也可以通过以上网站进行测试获得, 或者自行评估.<br><br>注意: 全部选择中庸(50%) 并不会给你带来任何匹配优势 (反而可能带来劣势)</div>"
        />
        <SliderElement
          name="mbti_ei"
          label="在MBTI“能量来源”维度中，你认为自己更偏向"
          :default="50"
          show-tooltip="drag"
          :min="0"
          :max="100"
          :step="1"
          :format="{
            suffix: '%',
          }"
          size="lg"
          :rules="['required']"
          after="<div style='display:flex; margin-block: 0.5rem 0.5rem; justify-content: space-between; padding-inline: 0.5rem;'>
  <p>E (外向)</p>
  <p>I (内向)</p>
  </div>"
        />
        <SliderElement
          name="mbti_sn"
          label="在MBTI“感知偏好”维度中，你认为自己更偏向"
          :default="50"
          show-tooltip="drag"
          :min="0"
          :max="100"
          :step="1"
          :format="{
            suffix: '%',
          }"
          size="lg"
          :rules="['required']"
          after="<div style='display:flex; margin-block: 0.5rem 0.5rem; justify-content: space-between; padding-inline: 0.5rem;'>
  <p>S (实感)</p>
  <p>N (直觉)</p>
  </div>"
        />
        <SliderElement
          name="mbti_tf"
          label="在MBTI“判断偏好”维度中，你认为自己更偏向"
          :default="50"
          show-tooltip="drag"
          :min="0"
          :max="100"
          :step="1"
          :format="{
            suffix: '%',
          }"
          size="lg"
          :rules="['required']"
          after="<div style='display:flex; margin-block: 0.5rem 0.5rem; justify-content: space-between; padding-inline: 0.5rem;'>
  <p>T (思考)</p>
  <p>F (情感)</p>
  </div>"
        />
        <SliderElement
          name="mbti_jp"
          label="在MBTI“行为模式”维度中，你认为自己更偏向"
          :default="50"
          show-tooltip="drag"
          :min="0"
          :max="100"
          :step="1"
          :format="{
            suffix: '%',
          }"
          size="lg"
          :rules="['required']"
          after="<div style='display:flex; margin-block: 0.5rem 0.5rem; justify-content: space-between; padding-inline: 0.5rem;'>
  <p>J (判断)</p>
  <p>P (感知)</p>
  </div>"
        />
        <StaticElement name="divider_2" tag="hr" top="2" />

        <StaticElement name="h2_2" tag="h2" content="你的匹配偏好" />
        <StaticElement name="h2_1" tag="h2" content="你的兴趣/ 爱好/ 想法" />
        <TagsElement
          name="hobbies"
          field-name="兴趣爱好"
          :close-on-select="false"
          :items="[
            {
              value: 'workout',
              label: '健身',
            },
            {
              value: 'read',
              label: '阅读',
            },
            {
              value: 'film',
              label: '看剧、电影',
            },
            {
              value: 'music',
              label: '音乐',
            },
            {
              value: 'travel',
              label: '旅游',
            },
            {
              value: 'photography',
              label: '摄影',
            },
            {
              value: 'acg',
              label: '二次元',
            },
            {
              value: 'vediogame',
              label: '游戏',
            },
            {
              value: 'sport',
              label: '运动',
            },
            {
              value: 'cook',
              label: '做饭',
            },
            {
              value: 'paint',
              label: '绘画',
            },
            {
              value: 'create',
              label: '创作',
            },
          ]"
          :native="false"
          label="选择你的爱好（多选）"
          :rules="['required']"
          :max="3"
          info="最多选择3个"
        />
        <RadiogroupElement
          name="travel_destination"
          field-name="期待的旅游地点"
          view="blocks"
          :items="[
            {
              value: 'sea',
              label: '海边 ',
              description: null,
            },
            {
              value: 'town',
              label: '安静宜人的小镇',
              description: null,
            },
            {
              value: 'city',
              label: '现代化大都市',
              description: null,
            },
            {
              value: 'none',
              label: '我不喜欢旅游',
              description: null,
            },
          ]"
          label="你更期待前往哪里旅游？
  "
          :rules="['required']"
        />
        <RadiogroupElement
          name="superpower"
          field-name="希望拥有的超能力"
          view="blocks"
          :items="[
            {
              value: 'animal',
              label: '能和所有动物交流',
              description: null,
            },
            {
              value: 'fly',
              label: '可以飞',
              description: null,
            },
            {
              value: 'mindreading',
              label: '读心术',
              description: null,
            },
            {
              value: 'prophecy',
              label: '可以预知1小时后的未来',
              description: null,
            },
            {
              value: 'resurrection',
              label: '可以复活一次',
              description: null,
            },
          ]"
          label="你最希望拥有哪种超能力？"
          :rules="['required']"
        />
        <RadiogroupElement
          name="use_of_money"
          field-name="如何处理意外财富"
          view="blocks"
          :items="[
            {
              value: 'invest',
              label: '投资理财',
              description: null,
            },
            {
              value: 'one_off',
              label: '旅行或购买心仪已久的东西',
              description: null,
            },
            {
              value: 'save',
              label: '储蓄起来，以备不时之需',
              description: null,
            },
            {
              value: 'daily',
              label: '摊开用来增加日常开销',
              description: null,
            },
            {
              value: 'charity',
              label: '捐赠给需要帮助的人',
              description: null,
            },
          ]"
          label="面对一笔意外的财富，你会？"
          :rules="['required']"
        />
        <RadiogroupElement
          name="family"
          field-name="原生家庭的重要性"
          view="blocks"
          :items="[
            {
              value: 2,
              label: '很重要，而且很难改变',
              description: null,
            },
            {
              value: 1,
              label: '重要，但是我们可以重塑自己',
              description: null,
            },
            {
              value: 0,
              label: '不重要，主要取决于自身',
              description: null,
            },
          ]"
          label="你觉得原生家庭对一个人的影响？"
          :rules="['required']"
        />
        <RadiogroupElement
          name="lifestyle"
          field-name="最喜欢的时代"
          view="blocks"
          :items="[
            {
              value: 'potter',
              label: '哈利波特',
              description: null,
            },
            {
              value: '1984',
              label: '1984',
              description: null,
            },
            {
              value: 'prince',
              label: '小王子',
              description: null,
            },
            {
              value: 'matrix',
              label: '黑客帝国',
              description: null,
            },
            {
              value: 'jurassic',
              label: '侏罗纪公园',
              description: null,
            },
            {
              value: 'gatsby',
              label: '了不起的盖茨比',
              description: null,
            },
          ]"
          label="你更愿意在哪个书或电影中生活一段时间？"
          :rules="['required']"
        />
        <StaticElement name="divider_3" tag="hr" top="2" />

        <StaticElement name="h3_2" tag="h3" content="硬性要求" />
        <StaticElement
          name="p_1"
          tag="p"
          content="<div>对于硬性要求, 我们将<strong>过滤掉</strong>不符合的人选<br>以下选项<strong>会减少</strong>你可匹配的人选数量</div>"
        />
        <RadiogroupElement
          name="preferred_sex"
          field-name="期望对方性别"
          view="tabs"
          :items="[
            {
              value: 'M',
              label: '男',
            },
            {
              value: 'F',
              label: '女',
            },
          ]"
          label="你要求对方的性别是"
          :rules="['required']"
        />
        <CheckboxgroupElement
          name="preferred_grades"
          field-name="期望对方年级"
          view="blocks"
          :items="[
            {
              value: 'UG1',
              label: '本科大一',
              description: null,
            },
            {
              value: 'UG2',
              label: '本科大二',
              description: null,
            },
            {
              value: 'UG3',
              label: '本科大三',
              description: null,
            },
            {
              value: 'UG4',
              label: '本科大四',
              description: null,
            },
            {
              value: 'UG5',
              label: '本科大五',
              description: null,
            },
            {
              value: 'PG',
              label: '硕/博士生',
              description: null,
            },
            {
              value: 'PROF',
              label: '教授',
              description: null,
            },
          ]"
          label="你接受对方的年级是（多选）"
          :rules="['required']"
        />
        <CheckboxgroupElement
          name="preferred_schools"
          field-name="期望对方就读学校"
          view="blocks"
          :items="[
            {
              value: 'HKU',
              label: 'HKU',
              description: null,
            },
            {
              value: 'CUHK',
              label: 'CUHK',
              description: null,
            },
            {
              value: 'UST',
              label: 'HKUST',
              description: null,
            },
          ]"
          label="你接受对方的学校是（多选）"
          :rules="['required']"
        />
        <StaticElement name="divider_4" tag="hr" top="1" bottom="1" />
        <StaticElement name="h3_3" tag="h3" content="软性要求" />
        <StaticElement
          name="p_3"
          tag="p"
          content="<div>对于软性要求, 你可能匹配到不符合你的选择的人选<br>以下选项<strong>不会减少</strong>你可匹配的人选数量</div>"
        />
        <RadiogroupElement
          name="preferred_mbti_ei"
          field-name="期望对方能量来源"
          view="tabs"
          :items="[
            {
              value: 'e',
              label: 'E 外向',
            },
            {
              value: 'x',
              label: '无偏好',
            },
            {
              value: 'i',
              label: 'I 内向',
            },
          ]"
          label="在MBTI“能量来源”维度中，你更希望对方是 "
          :rules="['required']"
        />
        <RadiogroupElement
          name="preferred_mbti_sn"
          field-name="期望对方感知偏好"
          view="tabs"
          :items="[
            {
              value: 's',
              label: 'S 实感',
            },
            {
              value: 'x',
              label: '无偏好',
            },
            {
              value: 'n',
              label: 'N 直觉',
            },
          ]"
          label="在MBTI“感知偏好”维度中，你更希望对方是"
          :rules="['required']"
        />
        <RadiogroupElement
          name="preferred_mbti_tf"
          field-name="期望对方判断偏好"
          view="tabs"
          :items="[
            {
              value: 't',
              label: 'T 思考',
            },
            {
              value: 'x',
              label: '无偏好',
            },
            {
              value: 'f',
              label: 'F 情感 ',
            },
          ]"
          label="在MBTI“判断偏好”维度中，你更希望对方是"
          :rules="['required']"
        />
        <RadiogroupElement
          name="preferred_mbti_jp"
          field-name="期望对方认知态度"
          view="tabs"
          :items="[
            {
              value: 'j',
              label: 'J 判断',
            },
            {
              value: 'x',
              label: '无偏好',
            },
            {
              value: 'p',
              label: 'P 感知',
            },
          ]"
          label="在MBTI“认知态度”维度中，你更希望对方是"
          :rules="['required']"
        />
        <StaticElement name="divider_6" tag="hr" top="1" bottom="1" />
        <StaticElement name="h3_4" tag="h3" content="心仪的人" />
        <TextElement
          name="preferred_wxid"
          label="如果你有想匹配的对象，请留下ta的微信号"
          description="（请注意，这并不保证100%成功，前提是对方也希望与你匹配）请确定微信号填写正确，且可被添加，请留下微信号而非电话号码，若有一方留下电话号码，而另一方留下微信号，系统将不能成功匹配."
          :rules="['max:50']"
        />
        <RadiogroupElement
          name="continue_match"
          field-name="是否继续匹配"
          view="tabs"
          label="如果和ta匹配失败，是否愿意继续随机匹配"
          :rules="['required']"
          :conditions="[['preferred_wxid', 'not_empty']]"
          :items="[
            {
              value: true,
              label: '是',
            },
            {
              value: false,
              label: '否',
            },
          ]"
        />
        <StaticElement name="divider_5" tag="hr" top="2" />

        <StaticElement name="h2_3" tag="h2" content="注意事项" />
        <StaticElement name="h3_11" tag="h3" content="自助提醒" />
        <StaticElement
          name="p_4"
          tag="p"
          content="<div>本次活动为半自助形式, 参与者需要访问本网址 (valentine.tripleuni.com)&nbsp; 获取匹配结果, 查看、提交每日任务等...<br><strong>Mentor将不会主动添加你, 请在网站上查看匹配结果</strong></div>"
        />
        <StaticElement name="h3_5" tag="h3" content="一周CP时间线" top="1" />
        <StaticElement
          name="p_5"
          tag="p"
          content="<div>2.1 19:00 开始报名<br>2.4 10:00 截止报名<br>2.4 19:00 公布第一轮匹配结果<br><strong>2.5 23:59 第一轮确认&amp;押金缴纳ddl<br></strong>2.6 08:00 公布第二轮匹配结果<br><strong>2.7 12:00 第二轮确认&amp;押金缴纳ddl<br></strong>2.7 22:00 双方可查看对方微信号并自主添加<br>2.8 00:00 第一天任务公布, 活动正式开始<br>...<br>2:14 23:59 第七天任务提交ddl, 活动结束<br><br><strong>请记录并及时查看每一轮的匹配结果</strong></div>"
        />
        <StaticElement name="divider_7" tag="hr" top="1" bottom="1" />
        <StaticElement name="h3_6" tag="h3" content="额外信息" />
        <TextareaElement
          name="comment"
          label="还有什么想补充的吗?"
          placeholder="请注意, 我们无法得知申请者的外貌/ 身高/ 性格等信息, 也无法根据此进行匹配"
          :rows="5"
        />
        <CheckboxElement
          name="confirm1"
          field-name="信息无误"
          text="我确认所填写的信息准确无误, 由信息填写错误而导致的任何问题, 我将负全部责任. 如果因为填写错误导致对方要求退出, 我的押金将全部 [不退还]"
          :submit="false"
          :rules="['accepted']"
        />
        <CheckboxElement
          name="confirm2"
          field-name="无法重新提交"
          :submit="false"
          :rules="['accepted']"
          text="我只能提交一次申请, 提交后我将无法取消/ 更改/ 重新提交申请"
        />
        <StaticElement name="divider_8" tag="hr" top="2" />
      </FormElements>

      <FormStepsControls />
    </template>
  </Vueform>
  <ModalLoading :model-value="showLoader" :text="loadingText" />
</template>

<script setup lang="ts">
interface VueformInstance {
  data: Record<string, any>;
  load(data: Record<string, any>): void;
}
const form$: Ref<null | VueformInstance> = ref(null);
const { postApplicant, fetchApplicantDetail, fetchApplicantId, patchApplicant } = useHttp();
const { setApplicantId, getApplicantId, clearApplicantId } = useStore();
const router = useRouter();
const showLoader = ref(true);
const loadingText: Ref<string | null> = ref(null);

async function handleSubmit() {
  if (!form$.value) {
    alert("表单初始化错误");
    return;
  }
  loadingText.value = "通知月老中";
  showLoader.value = true;
  const applicantId = getApplicantId();
  if (applicantId) {
    patchApplicant(applicantId, form$.value.data)
      .then(() => {
        router.push("/");
      })
      .catch((error: Error) => {
        alert("更新失败: " + error.message);
        showLoader.value = false;
        loadingText.value = null;
      });
    return
  }
  postApplicant(form$.value.data)
    .then((applicantId: string) => {
      setApplicantId(applicantId);
      router.push("/");
    })
    .catch((error: Error) => {
      alert("提交失败: " + error.message);
      showLoader.value = false;
      loadingText.value = null;
    });
}
async function onFormMounted() {
  let applicantId = getApplicantId();
  if (!applicantId) {
    loadingText.value = "查找你的档案中";
    showLoader.value = true;
    applicantId = await fetchApplicantId();
  }
  if (!applicantId) {
    showLoader.value = false;
    loadingText.value = null;
    return;
  }
  setApplicantId(applicantId);

  fetchApplicantDetail(applicantId)
    .then((data) => {
      if (!form$.value) {
        alert("表单初始化错误");
        return;
      }
      form$.value.load(data);
      showLoader.value = false;
      loadingText.value = null;
    })
    .catch((error: Error) => {
      clearApplicantId();
      alert("获取数据失败: " + error.message);
      showLoader.value = false;
      loadingText.value = null;
    });
}
function updateData() {
  // console.log("update");
}
</script>

<style scoped>
.vf-application-form *,
.vf-application-form *:before,
.vf-application-form *:after,
.vf-application-form:root {
  --vf-primary: var(--clr-primary);
  --vf-primary-darker: var(--clr-primary-dark);
  --vf-color-on-primary: #ffffff;

  --vf-color-passive: var(--clr-text--muted);

  /* slider */
  --vf-ring-width: 2px;
  --vf-ring-color: var(--clr-primary-light);
  --vf-slider-handle-size-lg: 1.75rem;

  --vf-font-size-h1: 2.125rem;
  --vf-font-size-h2: 1.875rem;
  --vf-font-size-h3: 1.5rem;
  --vf-font-size-h1-mobile: var(--fs-600);
  --vf-font-size-h2-mobile: var(--fs-600);
  --vf-font-size-h3-mobile: var(--fs-500);

  --vf-line-height: 1.5;
  --vf-line-height-headings: 1.2;
}
</style>
