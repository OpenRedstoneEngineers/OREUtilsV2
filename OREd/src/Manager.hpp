/**
 *  ORE Server management daemon
 *  Copyright (C) 2013 OpenRedstone
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#ifndef _ORED_MANAGER_
#define _ORED_MANAGER_

#include "ProtoServer.hpp"

#include "Console.hpp"

#include <map>
#include <string>

namespace OREd
{
	/**
	 * \brief Manages the server consoles.
	 */
	class Manager : public ProtoServer
	{
	public:
		typedef bool (*CmdHandler)(Client* cli, Console* target, const ArgsList& args);

		typedef std::map<const std::string, Console*> ConsoleMap;

		typedef std::map<const std::string, CmdHandler> HandlerMap;

	public:
		Manager(const int port, const std::string& name) : ProtoServer(port), m_Host(name) {}

		/**
		 * \brief Init a console instance.
		 */
		void InitConsole(const std::string& name, Console* console);

		/**
		 * \return the console with the specified name.
		 */
		Console* GetConsole(const std::string& name);

		/**
		 * \return the associated hostname.
		 */
		std::string GetHostname() const;

	protected:
		Console* GetConsoleByTarget(const std::string& target);

	protected:
		virtual bool OnCommand(Client* cli, const ArgsList& args);

		virtual bool OnEvent(Client* cli, const ArgsList& args);

		virtual bool OnQuery(Client* cli, const ArgsList& args);

	protected:
		/** Associated consoles */
		ConsoleMap m_Consoles;

		/** Command handlers */
		HandlerMap m_CmdHandlers;

		/** Query handlers */
		HandlerMap m_QueryHandlers;

		/** Associated host name */
		std::string m_Host;
	};

	std::string Manager::GetHostname() const
	{
		return m_Host;
	}
} /* OREd */

#endif
