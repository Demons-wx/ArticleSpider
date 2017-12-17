CREATE TABLE `jobbole_article` (
  `title` varchar(200) NOT NULL COMMENT '标题',
  `url` varchar(300) NOT NULL COMMENT '链接',
  `url_object_id` varchar(50) NOT NULL COMMENT 'url加密',
  `front_image_url` varchar(300) DEFAULT NULL COMMENT '头图',
  `front_image_path` varchar(200) DEFAULT NULL COMMENT '头图本地路径',
  `comment_nums` int(11) NOT NULL DEFAULT '0' COMMENT '评论数',
  `fav_nums` int(11) NOT NULL DEFAULT '0' COMMENT '收藏数',
  `praise_nums` int(11) NOT NULL DEFAULT '0' COMMENT '点赞数',
  `tags` varchar(200) DEFAULT NULL COMMENT '标签',
  `content` longtext COMMENT '文章内容',
  `create_date` date DEFAULT NULL COMMENT '创建日期',
  PRIMARY KEY (`url_object_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='文章表';


CREATE TABLE `zhihu_question` (
  `zhihu_id` bigint(20) NOT NULL DEFAULT '0' COMMENT '知乎id',
  `topics` varchar(255) DEFAULT NULL COMMENT '话题',
  `url` varchar(300) NOT NULL DEFAULT '' COMMENT '链接',
  `title` varchar(200) NOT NULL DEFAULT '' COMMENT '标题',
  `content` longtext NOT NULL COMMENT '正文',
  `crerate_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '修改时间',
  `answer_num` int(11) NOT NULL DEFAULT '0' COMMENT '回答数',
  `comments_num` int(11) NOT NULL DEFAULT '0' COMMENT '评论数',
  `watch_user_num` int(11) NOT NULL DEFAULT '0' COMMENT '关注人数',
  `click_num` int(11) NOT NULL DEFAULT '0' COMMENT '点击数',
  `crawl_time` datetime NOT NULL COMMENT '爬取时间',
  `crawl_update_time` datetime DEFAULT NULL COMMENT '爬取更新时间',
  PRIMARY KEY (`zhihu_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='知乎问题表';


CREATE TABLE `zhihu_answer` (
  `zhihu_id` bigint(20) NOT NULL DEFAULT '0' COMMENT '知乎id',
  `url` varchar(300) NOT NULL DEFAULT '' COMMENT '链接',
  `question_id` bigint(20) NOT NULL DEFAULT '0' COMMENT '问题id',
  `author_id` varchar(100) DEFAULT NULL COMMENT '用户id',
  `content` longtext NOT NULL COMMENT '正文',
  `praise_num` int(11) NOT NULL DEFAULT '0' COMMENT '点赞数',
  `comments_num` int(11) NOT NULL DEFAULT '0' COMMENT '评论数',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '修改时间',
  `crawl_time` datetime NOT NULL COMMENT '爬取时间',
  `crawl_update_time` datetime DEFAULT NULL COMMENT '爬取更新时间',
  PRIMARY KEY (`zhihu_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='知乎回答表';
