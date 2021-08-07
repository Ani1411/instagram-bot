from InstaBot import InstagramBot

if __name__ == '__main__':
    bot = InstagramBot('username', 'password')
    bot.login()
    bot.get_details_of_account('friend_username')


