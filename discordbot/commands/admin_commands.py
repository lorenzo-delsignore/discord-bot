from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role("Mod")
    async def kick(self, ctx, member: commands.MemberConverter, *, reason=None):
        try:
            await member.kick(reason=reason)
            await ctx.send(f"Kicked {member.display_name}!")
        except Exception as e:
            await ctx.send(f"Failed to kick {member.display_name}: {e}")

    @commands.command()
    @commands.has_role("Mod")
    async def ban(self, ctx, member: commands.MemberConverter, *, reason=None):
        try:
            await member.ban(reason=reason)
            await ctx.send(f"Banned {member.display_name}!")
        except Exception as e:
            await ctx.send(f"Failed to ban {member.display_name}: {e}")

    @commands.command()
    @commands.has_role("Mod")
    async def unban(self, ctx, *, member):
        try:
            banned_users = await ctx.guild.bans()
            member_name, member_discriminator = member.split("#")
            for ban_entry in banned_users:
                user = ban_entry.user
                if (user.name, user.discriminator) == (
                    member_name,
                    member_discriminator,
                ):
                    await ctx.guild.unban(user)
                    await ctx.send(f"Unbanned {user.mention}")
                    return
            await ctx.send(f"Member {member} not found in the ban list.")
        except ValueError:
            await ctx.send(
                "Invalid format. Please use Name#Discriminator (e.g., User#1234)."
            )
        except Exception as e:
            await ctx.send(f"Failed to unban {member}: {e}")


async def setup(bot):
    await bot.add_cog(Admin(bot))
