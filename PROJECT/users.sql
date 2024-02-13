-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema users
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema users
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `users` DEFAULT CHARACTER SET utf8 ;
USE `users` ;

-- -----------------------------------------------------
-- Table `users`.`users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `users`.`users` ;

CREATE TABLE IF NOT EXISTS `users`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `alias` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `password` VARCHAR(128) NOT NULL,
  `created_at` DATETIME NULL DEFAULT now(),
  `updated_at` DATETIME NULL DEFAULT now(),
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `users`.`ideas`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `users`.`ideas` ;

CREATE TABLE IF NOT EXISTS `users`.`ideas` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `content` TEXT NOT NULL,
  `created_at` DATETIME NULL DEFAULT now(),
  `updated_at` DATETIME NULL DEFAULT now(),
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_thoughts_usuario_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_thoughts_usuario`
    FOREIGN KEY (`user_id`)
    REFERENCES `users`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `users`.`likes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `users`.`likes` ;

CREATE TABLE IF NOT EXISTS `users`.`likes` (
  `user_id` INT NOT NULL,
  `idea_id` INT NOT NULL,
  `amount` INT NULL,
  PRIMARY KEY (`user_id`, `idea_id`),
  INDEX `fk_users_has_ideas_ideas1_idx` (`idea_id` ASC) VISIBLE,
  INDEX `fk_users_has_ideas_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_users_has_ideas_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `users`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_has_ideas_ideas1`
    FOREIGN KEY (`idea_id`)
    REFERENCES `users`.`ideas` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
