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
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='文章表'